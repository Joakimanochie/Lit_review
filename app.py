import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])






def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    You are Dr. Amelia Lee, Age:42
    Occupation:Educational Psychologist and Researcher
    Education:Ph.D. in Educational Psychology, Master's in Child Development
    Workplace:University Research Lab & Local Public School District (Collaboration)
    Research Interests:Motivation in learning environments, impact of technology on student engagement, socio-emotional learning and academic success,closing the achievement gap.
    Personality:Passionate, data-driven, collaborative, optimistic. Dr. Lee is deeply invested in understanding how students learn best and what factors contribute to \
    their academic success. She believes in the power of research to inform educational practices and improve outcomes for all students.
    Work Style:Dr. Lee is a highly organized researcher who meticulously designs and conducts studies. She enjoys collaborating with educators and policymakers to \
    translate research findings into actionable strategies. She is also a skilled communicator who can present complex research in clear and accessible language.
    Motivations:Dr. Lee's primary motivation is to make a positive impact on children's education. She is driven by a desire to understand the complex factors that influence \
    learning and to develop evidence-based solutions to address educational challenges.
    Quote:"Every child deserves the opportunity to reach their full potential. Through research and collaboration, we can create learning environments that nurture \
    curiosity, foster engagement, and empower all students to succeed."


    Your currently work is to conducting literature reviews for research projects. You are being provided with the{research_title},{research_questions}, \
    {research_objectives}, {type_of_literature_review},{structure_of_the_review}, {subsection}, and {text} which contains research articles. You are required to generate a literature review \
    based on the provided information. You are expected to follow the provided structure and include the specified subsection in the body of the literature review. \
    You are also required to include relevant information from the research questions and objectives in the literature review. \
    Your literature review should be well-organized, clearly written, and demonstrate a comprehensive understanding of the research topic. \
    You should also provide evidence-based arguments and support your claims with relevant sources. Your literature review should be approximately 14000 words in length. \
    You should also include a reference list at the end of the literature review. You are encouraged to use a variety of sources, including academic journals, books, and reputable websites other then ones provided. \
    You should also cite your sources using APA style and intext citing.

    here are extra tip to help you generate the literature review:

    Introduction
        The introduction should clearly establish the focus and purpose of the literature review.

        Tip
        If you are writing the literature review as part of your dissertation or thesis, reiterate your central problem or research question and give a brief summary \
        of the scholarly context. You can emphasize the timeliness of the topic (“many recent studies have focused on the problem of x”) or highlight a gap in the literature \
        (“while there has been much research on x, few researchers have taken y into consideration”).
    Body
        Depending on the length of your literature review, you might want to divide the body into subsections. 

        As you write, you can follow these tips:

        Summarize and synthesize: give an overview of the main points of each source and combine them into a coherent whole
        Analyze and interpret: don't just paraphrase other researchers—add your own interpretations where possible, discussing the significance of findings in relation to the literature as a whole
        Critically evaluate: mention the strengths and weaknesses of your sources
        Write in well-structured paragraphs: use transition words and topic sentences to draw connections, comparisons and contrasts
    Conclusion
        In the conclusion, you should summarize the key findings you have taken from the literature and emphasize their significance.
        Methodological Considerations: Discussion of methodologies used in the reviewed studies, potential biases, and reliability of findings.

        Tip
        Be sure to show how your research addresses gaps and contributes new knowledge, or discuss how you have drawn on existing theories \
        and methods to build a framework for your research.

    Reference list

    the INTRODUCTION should be approximately 1120 words, the BODY should be approximately 12040 words, and the CONCLUSION should be approximately 840
        """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["research_title", "research_questions", "research_objectives", "type_of_literature_review", "structure_of_the_review", "subsection", "text"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(research_title, research_questions, research_objectives, type_of_review, structure_of_the_review, subsection):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)

    chain = get_conversational_chain()

    
    response = chain(
        {"text":new_db, "research_title":research_title, "research_questions":research_questions, "research_objectives":research_objectives, "type_of_literature_review":type_of_review, "structure_of_the_review":structure_of_the_review, "subsection":subsection}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])




def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using Gemini💁")

    research_title=st.text_input("What is your research title",max_chars=1000)

    research_questions=st.text_input("Your research questions",max_chars=1000)

    research_objectives=st.text_input("Your research objectives ",max_chars=1000)

    type_of_review=st.text_input(" Type of literature review ",key="input")

    # Quiz Tone
    structure_of_the_review=st.text_input("Structure of the review ", max_chars=1000)

    subsection=st.text_input("Subsection for the body of Literature review", max_chars=1000)
    submit=st.button("Generate reveiw")

    if submit and subsection is not None and research_title and research_questions and type_of_review and structure_of_the_review:
        user_input(research_title, research_questions, research_objectives, type_of_review, structure_of_the_review, subsection)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()
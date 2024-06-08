from dotenv import load_dotenv

load_dotenv() ## load all the environment variables
import traceback
import streamlit as st
import os
import PyPDF2
import json
import google.generativeai as genai
import pandas as pd

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def read_files(files):
    """
    Reads and extracts text from multiple files (PDF or text).

    Args:
        files (list): List of file objects (PDF or text files).

    Returns:
        list: List of extracted texts from each file.
    """
    extracted_texts = []
    for file in files:
        if file.name.endswith(".pdf"):
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                extracted_texts.append(text)
            except Exception as e:
                raise Exception(f"Error reading the PDF file: {e}")
        elif file.name.endswith(".txt"):
            extracted_texts.append(file.read().decode("utf-8"))
        else:
            raise Exception("Unsupported file format. Only PDF and text files are supported.")
    return extracted_texts

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(prompt, research_title, research_questions, research_objectives, type_of_review, structure_of_the_review, subsection):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt, research_title, research_questions, research_objectives, type_of_review, structure_of_the_review, subsection])
    return response.text


##initialize our streamlit app

st.set_page_config(page_title="Class Help")

st.header("Class Help")
#Subject
#uploaded_file=st.file_uploader("Uplaod a PDF or txt file", accept_multiple_files=True)

#Subject
research_title=st.text_input("What is your research title",max_chars=1000)

research_questions=st.text_input("Your research questions",max_chars=1000)

research_objectives=st.text_input("Your research objectives ",max_chars=1000)

type_of_review=st.text_input(" Type of literature review ",key="input")

# Quiz Tone
structure_of_the_review=st.text_input("Structure of the review ", max_chars=1000)

subsection=st.text_input("Subsection for the body of Literature review", max_chars=1000)

submit=st.button("Generate reveiw")

input_prompt="""
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
{research_objectives}, {type_of_literature_review},{structure_of_the_review}, {subsection}. You are required to generate a literature review \
based on the provided information. You are expected to follow the provided structure and include the specified subsection in the body of the literature review. \
You are also required to include relevant information from the research questions and objectives in the literature review. \
Your literature review should be well-organized, clearly written, and demonstrate a comprehensive understanding of the research topic. \
You should also provide evidence-based arguments and support your claims with relevant sources. Your literature review should be approximately 14000 words in length. \
You should also include a reference list at the end of the literature review. You are encouraged to use a variety of sources, including academic journals, books, and reputable websites that reflect \
the independent variables, dependent variables, and thier sub-variables. \
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

## If submit button is clicked

if submit and subsection is not None and research_title and research_questions and type_of_review and structure_of_the_review and research_objectives:
        with st.spinner("loading..."):
            try:
                #text = read_files(uploaded_file)
        
                response=get_gemini_repsonse(input_prompt, research_title, research_questions, research_objectives, type_of_review, structure_of_the_review, subsection)
                st.subheader("Literature Review Generated")
                st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

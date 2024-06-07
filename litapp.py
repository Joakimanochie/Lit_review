from dotenv import load_dotenv

load_dotenv() ## load all the environment variables
import traceback
import streamlit as st
import os
import google.generativeai as genai
from utils import read_file
import pandas as pd

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(prompt,text):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt,text])
    return response.text


##initialize our streamlit app

st.set_page_config(page_title="Class Help")

st.header("Class Help")
#Subject
uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

#Subject
research_title=st.text_input("What is your research title",max_chars=20)

research_questions=st.text_input("Your research questions",max_chars=20)

type_of_review=st.text_input(" Type of literature review ",key="input")

# Quiz Tone
structure_of_the_review=st.text_input("Structure of the review ", max_chars=20, placeholder="Simple")

subsection=st.text_input("Subsection for the body of Literature review", min_value=3, max_value=50)

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

Your currently work is to conducting literature reviews for research projects. You are being provide with the :
"""

## If submit button is clicked

if submit and uploaded_file is not None and research_title and research_questions and type_of_review and structure_of_the_review:
        with st.spinner("loading..."):
            try:
                response=get_gemini_repsonse(input_prompt,text)
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

import streamlit as st
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.llms import OpenAI

# Load environment variables
load_dotenv()

# Set up the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Please set it in your environment variables.")


# Initialize LangChain with OpenAI
config = {
    "llm": {
        "type": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": OPENAI_API_KEY
    }
}
openai_llm = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'])
# Set up the Streamlit app


st.markdown("""
# 📝 AI-Powered Cover Letter Generator

Generate a cover letter. All you need to do is:
1. Upload your resume or copy your resume/experiences
2. Paste a relevant job description
3. Input some other relevant user/job data
""")

# radio for upload or copy paste option         
res_format = st.radio(
    "Do you want to upload or paste your resume/key experience",
    ('Upload', 'Paste'))

if res_format == 'Upload':
    # upload_resume
        res_file = st.file_uploader('📁 Upload your resume in pdf format')
        if res_file:
            pdf_reader = PdfReader(res_file)

            # Collect text from pdf
            res_text = ""
            for page in pdf_reader.pages:
                res_text += page.extract_text()
else:
    res_text = st.text_input('Pasted resume elements')

with st.form('input_form'):
    # other inputs
    job_desc = st.text_input('Pasted job description')
    user_name = st.text_input('Your name')
    company = st.text_input('Company name')
    manager = st.text_input('Hiring manager')
    role = st.text_input('Job title/role')
    referral = st.text_input('How did you find out about this opportunity?')
    ai_temp = st.number_input('AI Temperature (0.0-1.0) Input how creative the API can be',value=.99)

    # submit button
    submitted = st.form_submit_button("Generate Cover Letter")


# When the form is submitted
if submitted:
    try:
        # Preparing the prompt for the language model
        prompt = f"""
        You will need to generate a cover letter based on specific resume and a job description.
        My resume text: {res_text}
        The job description is: {job_desc}
        The candidate's name to include on the cover letter: {user_name}
        The job title/role: {role}
        The hiring manager is: {manager}
        How you heard about the opportunity: {referral}
        The company to which you are generating the cover letter for: {company}
        The cover letter should have three content paragraphs.
        In the first paragraph, focus on who you are, what position you are interested in, where you heard about it, and summarize what you have to offer.
        In the second paragraph, focus on why the candidate is a great fit, drawing parallels between the resume experience and the job description qualifications.
        In the third paragraph, restate your interest in the organization and/or job, summarize what you have to offer, and thank the reader.
        Use {user_name} as the candidate.
        Generate a specific cover letter based on the above.
        """

        # Generating the cover letter using LangChain's OpenAI LLM

        response = openai_llm(prompt, temperature=ai_temp, max_tokens=1024)

        # Displaying the generated cover letter
        st.write(response)

        # Option to download the cover letter
        st.download_button('Download the Cover Letter', response)

    except Exception as e:
        st.error(f"An error occurred: {e}")


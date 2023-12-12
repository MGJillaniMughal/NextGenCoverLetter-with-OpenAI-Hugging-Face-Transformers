import streamlit as st
import os
import openai as ai
from PyPDF2 import PdfReader
from openai import ChatCompletion

# Initialize the OpenAI API with your API key
ChatCompletion.api_key = 'OpenAI API Key'

st.markdown("""
# 📝 AI-Powered Cover Letter Generator

Generate a cover letter. All you need to do is:
1. Upload your resume or copy your resume/experiences
2. Paste a relevant job description
3. Input some other relevant user/job data
"""
)

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



# if the form is submitted run the openai completion   
if submitted:
    try:
            

        # note that the ChatCompletion is used as it was found to be more effective to produce good results
        # using just Completion often resulted in exceeding token limits
        # according to https://platform.openai.com/docs/models/gpt-3-5
        # Our most capable and cost effective model in the GPT-3.5 family is gpt-3.5-turbo which has been optimized for chat 
        # but works well for traditional completions tasks as well.
        # note that the turbo model is not available for the free tier

        completion = ChatCompletion.create(
        
        #model="gpt-3.5-turbo-16k", 
        model = "gpt-3.5-turbo-1106",
        temperature=ai_temp,
        messages = [
            {"role": "user", "content" : f"You will need to generate a cover letter based on specific resume and a job description"},
            {"role": "user", "content" : f"My resume text: {res_text}"},
            {"role": "user", "content" : f"The job description is: {job_desc}"},
            {"role": "user", "content" : f"The candidate's name to include on the cover letter: {user_name}"},
            {"role": "user", "content" : f"The job title/role : {role}"},
            {"role": "user", "content" : f"The hiring manager is: {manager}"},
            {"role": "user", "content" : f"How you heard about the opportunity: {referral}"},
            {"role": "user", "content" : f"The company to which you are generating the cover letter for: {company}"},
            {"role": "user", "content" : f"The cover letter should have three content paragraphs"},
            {"role": "user", "content" : f""" 
            In the first paragraph focus on the following: you will convey who you are, what position you are interested in, and where you heard
            about it, and summarize what you have to offer based on the above resume
            """},
                {"role": "user", "content" : f""" 
            In the second paragraph focus on why the candidate is a great fit drawing parallels between the experience included in the resume 
            and the qualifications on the job description.
            """},
                    {"role": "user", "content" : f""" 
            In the 3RD PARAGRAPH: Conclusion
        Restate your interest in the organization and/or job and summarize what you have to offer and thank the reader for their time and consideration.
            """},
            {"role": "user", "content" : f""" 
            note that contact information may be found in the included resume text and use and/or summarize specific resume context for the letter
                """},
            {"role": "user", "content" : f"Use {user_name} as the candidate"},
            
            {"role": "user", "content" : f"Generate a specific cover letter based on the above. Generate the response and include appropriate spacing between the paragraph text"}
        ]
        )
        #st.write(completion)
        response_out = completion['choices'][0]['message']['content']
        st.write(response_out)

        # include an option to download a txt file
        st.download_button('Download the cover_letter', response_out)
    except Exception as e:
        st.error(f"An error occurred: {e}")

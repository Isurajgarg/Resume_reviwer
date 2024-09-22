import google.generativeai as genai
import streamlit as st
import PyPDF2 as pdf 
from dotenv import load_dotenv
import os

load_dotenv()


genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))

def get_response(uploded_file,Job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    def text_get(uploded_file):
        reader = pdf.PdfReader(uploded_file)
        text =''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text +=  page.extract_text()
        return text
    text = text_get(uploded_file)
    input_prompt = '''You are an advanced AI system specialized in Application Tracking Systems (ATS) analysis. Given a resume and a job description, your task is to perform a comprehensive evaluation and provide the following:
1. **ATS Score:**
   - Analyze the resume in the context of the job description.
   - Calculate an ATS score that reflects how well the resume matches the job requirements. This score should consider factors such as keywords, relevant experience, education, and skills alignment.
   - The ATS score should be expressed as a percentage or numerical value, representing the degree of alignment between the applicant's qualifications and the job requirements.Ensure that scorereflects the true aligment not a generic range. Don't just 50-60 percent. Note if resume not match the resume say you not have these skills and give low range of score as well like 20-30 or whatever you finds sutiable.But when it match so show sore accordingly.
   in brief if resume doesn't match give low score and matches give high score accordingly
2. **Missing Skills and Qualifications:**
   - Review the job description to identify key skills, qualifications,Experince, and competencies required for the position.
   - Compare these requirements with the content of the resume.
   - Identify and list any critical skills, qualifications, or competencies mentioned in the job description that are missing or inadequately represented in the resume.
   - Provide specific examples from the job description that are not covered in the resume.
3. **Additional Insights:**
   - Offer insights into the overall suitability of the resume for the job position.
   - Highlight any strengths of the resume that align well with the job description.
   - Suggest areas for improvement in the resume to better match the job requirements.


4 **Summary of Lacking Areas:**
       - Summarize the key areas where the resume is lacking compared to the job description.
       - Offer a brief but clear summary that points out the gaps in skills, qualifications, or experience.

5. **Resources for Skill Development:**
       - For each skill or qualification that is missing or underrepresented, suggest specific resources to help the applicant learn or improve in that area. 
       - Resources can include links to online courses, tutorials, documentation,Youtube Videos or books related to the skill (e.g., Udemy, Coursera, LinkedIn Learning,YouTube Videos or free documentation/tutorials) for each resource provide the link of that resource also.

6. **Additional Insights:**
       - Offer insights into the overall suitability of the resume for the job position.
       - Highlight any strengths of the resume that align well with the job description.
       - Suggest areas for improvement in the resume to better match the job requirements.
Ensure that your analysis is thorough and provides actionable feedback. Your evaluation should help in understanding how well the applicant's resume fits the job description and what improvements could be made to enhance the chances of passing through an ATS filter. '''
    response = model.generate_content(text + input_prompt +Job_description)
    return response.text

st.title('Application Tracking System (ATS) by Suraj Garg')

st.write('''
This tool is designed to analyze a resume in comparison to a given job description. It calculates an ATS (Application Tracking System) score to determine how well the resume matches the job requirements. Additionally, it identifies missing skills, qualifications, and competencies, and provides resources for improving in those areas. The goal is to help candidates improve their resumes and increase their chances of passing through ATS filters in job applications.
''')
resume_file = st.file_uploader("Choose a resume (PDF file)", type="pdf")

# Text area for job description
job_description = st.text_area("Enter the job description")

if st.button("Generate ATS Analysis"):
    if resume_file is not None and job_description:
        st.write(f"Uploaded Resume: {resume_file.name}")
        with st.spinner("Generating analysis..."):
            # Get the ATS analysis response
            ats_analysis = get_response(resume_file, job_description)
            st.subheader("ATS Analysis:")
            st.write(ats_analysis)
    else:
        st.error("Please upload a resume and enter a job description before submitting.")

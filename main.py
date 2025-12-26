import os
import zipfile
import tempfile
from typing import Optional, List

import streamlit as st
import pandas as pd
import fitz
from docx import Document
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
)



class ResumeSchema(BaseModel):
    summary: str = Field(description="Short professional summary")
    experience: Optional[int] = Field(default=None, description="Years of experience if mentioned")
    skills: List[str] = Field(description="List of technical skills")
    links: List[str] = Field(default=[], description="Any URLs like LinkedIn or GitHub")


structured_model = model.with_structured_output(ResumeSchema)


def read_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


st.set_page_config(page_title=" Resume Analyzer", layout="centered")
st.title("📄 Powered Resume Analyzer")
st.write("Upload a ZIP file containing PDF or DOCX resumes.")


uploaded_zip = st.file_uploader("Upload Resume ZIP", type=["zip"])


if uploaded_zip:
    extracted_data = []

    with st.spinner("Analyzing resumes using Gemini..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "resumes.zip")

            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.read())

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)

                if file_name.lower().endswith(".pdf"):
                    resume_text = read_pdf(file_path)
                elif file_name.lower().endswith(".docx"):
                    resume_text = read_docx(file_path)
                else:
                    continue

                try:
                    result = structured_model.invoke(resume_text)
                    data = result.model_dump()
                    data["file_name"] = file_name
                    extracted_data.append(data)
                except Exception as e:
                    st.error(f"❌ Error processing {file_name}: {e}")

    if extracted_data:
        df = pd.DataFrame(extracted_data)
        st.success("Resume analysis completed!")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="resume_analysis.csv",
            mime="text/csv",
        )
    else:
        st.warning("No resumes could be processed.")

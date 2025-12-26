# Automated Resume Analyzer

An AI-powered Resume Analyzer that processes multiple resumes from a ZIP file and extracts structured information using Large Language Models.

---

## Project Overview

Recruiters and HR teams often receive resumes in bulk, typically as ZIP files containing multiple PDF or DOCX resumes.  
Manually reviewing and extracting information from each resume is time-consuming and inconsistent.

This project automates resume analysis by converting unstructured resume text into structured data using Gemini LLM and LangChain-style structured output.

---

## Key Features

- Upload a ZIP file containing multiple resumes
- Supports PDF and DOCX resume formats
- Automatically extracts:
  - Professional summary
  - Years of experience (if available)
  - Skills
  - Profile links (LinkedIn, GitHub, etc.)
- Uses structured output validation with Pydantic
- Displays extracted data in a table
- Allows CSV download of results
- Simple and interactive Streamlit interface

---

## Tech Stack

- Python
- Streamlit
- Google Gemini LLM
- LangChain (Google GenAI integration)
- Pydantic
- Pandas
- PyMuPDF (PDF parsing)
- python-docx

---

## How It Works

1. User uploads a ZIP file containing resumes
2. Each resume is extracted and read based on file type (PDF or DOCX)
3. Resume text is sent to Gemini LLM
4. Structured information is generated using a defined schema
5. Results are displayed and can be downloaded as a CSV file

---

## Environment Setup

Create a `.env` file in the project root directory and add:


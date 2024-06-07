import os
import PyPDF2
import json
import traceback

import PyPDF2

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

import PyPDF2

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

# Example usage:
# files_list = [file1, file2, ...]  # List of file objects
# extracted_texts = read_files(files_list)
# print(extracted_texts)



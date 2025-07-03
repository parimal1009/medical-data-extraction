from pdf2image import convert_from_path
import pytesseract
import utils
from parser_patient_details import PatientDetailsParser
from parser_prescription import PrescriptionParser
import pandas as pd
import os
import re

POPPLER_PATH = r"C:/poppler-24.02.0/Library/bin"
TESSERACT_ENGINE_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_ENGINE_PATH

def extract(file_path, file_format):
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ""

    for page in pages:
        processed_image = utils.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang="eng")
        document_text += "\n" + text

    if file_format == "prescription":
        extracted_data = PrescriptionParser(document_text).parse()
        extracted_data['provisional_diagnosis'] = extract_provisional_diagnosis(document_text)
    elif file_format == "patient_details":
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f"Invalid file format: {file_format}")

    return extracted_data

def extract_provisional_diagnosis(text):
    diagnosis_match = re.search(r'(?i)provisional\s*diagnosis\s*[:\-\s]*([\w\s,.-]+(?:\n[\w\s,.-]+)*)', text)
    if diagnosis_match:
        return diagnosis_match.group(1).strip()
    else:
        return ""

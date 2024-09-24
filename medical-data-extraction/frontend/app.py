import streamlit as st
import requests
from pdf2image import convert_from_bytes
import time
import io
import pandas as pd
from streamlit_lottie import st_lottie

POPPLER_PATH = r"C:/poppler-24.02.0/Library/bin"
URL = "http://127.0.0.1:8000/extract_from_doc"

# Set page config
st.set_page_config(page_title="Medical Data Extractor", page_icon="🏥", layout="wide")

# Custom CSS for dark mode
st.markdown("""
<style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #1e1e1e;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #373737;
    }
    .stTextInput>div>div>input {
        background-color: #2e2e2e;
        color: #ffffff;
        border-radius: 5px;
    }
    .stRadio>div {
        background-color: #2e2e2e;
        padding: 10px;
        border-radius: 10px;
    }
    .stDataFrame {
        background-color: #2e2e2e;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput>div>label {
        color: #ffffff;
    }
    .stRadio>div>label {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Lottie animation
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_medical = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")

# Title with Lottie animation
col1, col2 = st.columns([1, 3])
with col1:
    st_lottie(lottie_medical, height=150, key="medical_animation")
with col2:
    st.title("Medical Data Extractor 🏥")

st.markdown("---")

# File uploader and document type selector
col3, col4 = st.columns(2)
with col3:
    file = st.file_uploader("Upload PDF file", type="pdf")
with col4:
    file_format = st.radio(label="Select type of document", options=["prescription", "patient_details"],
                           horizontal=True)

if file and st.button("Process PDF", type="primary"):
    with st.spinner("Processing..."):
        time.sleep(3)

    payload = {'file_format': file_format}
    files = {'file': file.getvalue()}
    headers = {}

    # Send file to backend and get the response (Excel file)
    response = requests.post(URL, headers=headers, data=payload, files={'file': file})

    if response.status_code == 200:
        # Read the Excel file content from the response
        excel_file = io.BytesIO(response.content)

        # Provide a download button for the Excel file
        st.download_button(label="Download Excel", data=excel_file, file_name="extracted_data.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Read the Excel file content as a pandas DataFrame and display it
        excel_file.seek(0)  # Reset the pointer to the beginning of the file
        df = pd.read_excel(excel_file)
        st.dataframe(df)  # Display the content in a table format

    else:
        st.error("Failed to extract data from the PDF.")

if file:
    st.markdown("---")
    pages = convert_from_bytes(file.getvalue(), poppler_path=POPPLER_PATH)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Document")
        st.image(pages[0], use_column_width=True)

    with col2:
        if st.session_state:
            st.subheader("Extracted Details")
            details_container = st.container()
            with details_container:
                if file_format == "prescription":
                    name = st.text_input(label="Name", value=st.session_state.get("patient_name", ""))
                    address = st.text_input(label="Address", value=st.session_state.get("patient_address", ""))
                    medicines = st.text_input(label="Medicines", value=st.session_state.get("medicines", ""))
                    directions = st.text_input(label="Directions", value=st.session_state.get("directions", ""))
                    refill = st.text_input(label="Refill", value=st.session_state.get("refill", ""))
                if file_format == "patient_details":
                    name = st.text_input(label="Name", value=st.session_state.get("patient_name", ""))
                    phone = st.text_input(label="Phone No.", value=st.session_state.get("phone_no", ""))
                    vacc_status = st.text_input(label="Hepatitis B vaccination status",
                                                value=st.session_state.get("vaccination_status", ""))
                    med_problems = st.text_input(label="Medical Problems", value=st.session_state.get("medical_problems", ""))
                    has_insurance = st.text_input(label="Insurance Status",
                                                  value=st.session_state.get("has_insurance", ""))

            if st.button(label="Submit", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success('Details successfully recorded.')

st.markdown("---")
st.markdown("© 2024 Medical Data Extractor. All rights reserved.")

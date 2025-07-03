import streamlit as st
import requests
from pdf2image import convert_from_bytes
import time
import io
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

POPPLER_PATH = r"C:/poppler-24.02.0/Library/bin"
URL = "http://127.0.0.1:8000/extract_from_doc"

# Set page config
st.set_page_config(page_title="Medical Data Extractor", page_icon="🏥", layout="wide")

# Custom CSS for improved dark mode
st.markdown("""<style>/* Custom styling */</style>""", unsafe_allow_html=True)

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
    st.subheader("Extract and analyze medical information with ease")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = "Upload"

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=["Upload", "Process", "Results"],
    icons=["cloud-upload", "gear", "clipboard-data"],
    menu_icon="cast",
    default_index=["Upload", "Process", "Results"].index(st.session_state['page']),
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#2e2e2e", "border-radius": "15px"},
        "icon": {"color": "#4CAF50", "font-size": "18px"},
        "nav-link": {"color": "#ffffff", "font-size": "16px", "text-align": "center", "margin": "0px",
                     "--hover-color": "#45a049"},
        "nav-link-selected": {"background-color": "#4CAF50"},
    }
)

# Update session state based on selection
st.session_state['page'] = selected

if st.session_state['page'] == "Upload":
    st.markdown("## Upload Your Document")
    file = st.file_uploader("Choose a PDF file", type=["pdf"],
                            help="Only upload a medical report or prescription in PDF format")

    if file:
        st.success("File uploaded successfully!")
        st.session_state['file'] = file

        st.markdown("### Document Type")
        file_format = st.radio(
            label="Select the type of document",
            options=["prescription", "patient_details"],
            format_func=lambda x: x.capitalize(),
            horizontal=True,
            help="Choose the appropriate document type for accurate extraction"
        )

        st.markdown("### Preview")
        pages = convert_from_bytes(file.getvalue(), poppler_path=POPPLER_PATH)
        st.image(pages[0], use_column_width=False, width=300, caption="Document Preview", output_format="PNG", clamp=True)

        st.session_state['file_format'] = file_format.lower()

        if st.button("Proceed to Processing", type="primary"):
            st.session_state['page'] = "Process"
            st.rerun()
    else:
        st.warning("Please upload a PDF file. Other formats are not supported.")

elif st.session_state['page'] == "Process":
    if 'file' not in st.session_state or 'file_format' not in st.session_state:
        st.warning("Please upload a document first.")
        if st.button("Go to Upload"):
            st.session_state['page'] = "Upload"
            st.rerun()
    else:
        st.markdown("## Process Document")
        st.info(f"Processing {st.session_state['file_format'].capitalize()} document")

        if st.button("Extract Data", type="primary"):
            with st.spinner("Processing..."):
                time.sleep(2)  # Simulating processing time

            payload = {'file_format': st.session_state['file_format']}
            files = {'file': st.session_state['file'].getvalue()}
            headers = {}
            response = requests.post(URL, headers=headers, data=payload, files=files)

            if response.status_code == 200:
                excel_file = io.BytesIO(response.content)
                excel_file.seek(0)
                df = pd.read_excel(excel_file)

                expected_columns = {
                    "prescription": ["provisional_diagnosis"],
                }

                for column in expected_columns[st.session_state['file_format']]:
                    if column not in df.columns:
                        df[column] = ""

                for column in df.columns:
                    st.session_state[column] = df[column].iloc[0] if not df[column].empty else ""

                st.session_state['processed_data'] = df
                st.success("Data extracted successfully!")
                st.session_state['page'] = "Results"
                st.rerun()
            else:
                st.error("Failed to extract data from the document. Please try again.")

elif st.session_state['page'] == "Results":
    if 'processed_data' not in st.session_state:
        st.warning("No processed data available. Please upload and process a document first.")
        if st.button("Go to Upload"):
            st.session_state['page'] = "Upload"
            st.rerun()
    else:
        st.markdown("## Extracted Results")

        tab1, tab2 = st.tabs(["Extracted Details", "Download Data"])

        with tab1:
            st.subheader("Extracted Information")
            details_container = st.container()
            with details_container:
                if st.session_state['file_format'] == "prescription":
                    st.text_input("Provisional Diagnosis", value=st.session_state.get("provisional_diagnosis", ""),
                                  disabled=True)

        with tab2:
            st.subheader("Download Extracted Data")
            if 'processed_data' in st.session_state:
                excel_file = io.BytesIO()
                st.session_state['processed_data'].to_excel(excel_file, index=False)
                excel_file.seek(0)
                st.download_button(
                    label="Download Excel",
                    data=excel_file,
                    file_name="extracted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

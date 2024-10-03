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
st.markdown("""
<style>
    .stApp {
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.3);
    }
    .stTextInput>div>div>input {
        color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    .stRadio>div {
        background-color: #2e2e2e;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #4CAF50;
    }
    .stDataFrame {
        border-radius: 15px;
        padding: 15px;
    }
    .stTextInput>div>label, .stRadio>div>label {
        color: #4CAF50;
        font-weight: bold;
    }
    .stTab {
        background-color: #2e2e2e;
        color: #ffffff;
        border-radius: 10px 10px 0 0;
    }
    .stTab[data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e1e1e;
        border: 1px solid #4CAF50;
        border-bottom: none;
    }
    .stTab[aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .preview-image {
        max-width: 300px;
        margin: auto;
        display: block;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .stAlert {
        background-color: #2e2e2e;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #4CAF50;
    }
    /* Custom CSS for option menu */
    .custom-option-menu {
        background-color: #2e2e2e;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .custom-option-menu .stSelectbox>div>div {
        background-color: #1e1e1e;
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
    file = st.file_uploader("Choose a PDF file", type="pdf", help="Upload a prescription or patient details document")

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
        st.image(pages[0], use_column_width=False, width=300, caption="Document Preview", output_format="PNG",
                 clamp=True)

        st.session_state['file_format'] = file_format.lower()

        if st.button("Proceed to Processing", type="primary"):
            st.session_state['page'] = "Process"
            st.rerun()

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
            headers={}
            response = requests.post(URL, headers=headers, data=payload, files=files)

            if response.status_code == 200:
                excel_file = io.BytesIO(response.content)
                excel_file.seek(0)
                df = pd.read_excel(excel_file)

                # Ensure all expected columns are present
                expected_columns = {
                    "prescription": ["patient_name", "patient_address", "medicines", "refill", "directions"],
                    "patient_details": ["patient_name", "phone_no", "has_insurance", "vaccination_status",
                                        "medical_problems"]
                }

                for column in expected_columns[st.session_state['file_format']]:
                    if column not in df.columns:
                        df[column] = ""  # Add missing column with empty string

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
                    st.text_input("Name", value=st.session_state.get("patient_name", ""), disabled=True)
                    st.text_input("Address", value=st.session_state.get("patient_address", ""), disabled=True)
                    st.text_area("Medicines", value=st.session_state.get("medicines", ""), disabled=True, height=100)
                    st.text_input("Refill", value=st.session_state.get("refill", ""), disabled=True)
                    st.text_area("Directions", value=st.session_state.get("directions", ""), disabled=True, height=100)
                elif st.session_state['file_format'] == "patient_details":
                    st.text_input("Name", value=st.session_state.get("patient_name", ""), disabled=True)
                    st.text_input("Phone No.", value=st.session_state.get("phone_no", ""), disabled=True)
                    st.text_input("Insurance Status", value=st.session_state.get("has_insurance", ""), disabled=True)
                    st.text_input("Hepatitis B Vaccination Status", value=st.session_state.get("vaccination_status", ""), disabled=True)
                    st.text_area("Medical Problems", value=st.session_state.get("medical_problems", ""), disabled=True, height=100)

        with tab2:
            st.subheader("Download Extracted Data")
            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                st.session_state['processed_data'].to_excel(writer, index=False, sheet_name='Sheet1')
            excel_file.seek(0)

            st.download_button(
                label="Download Excel",
                data=excel_file,
                file_name="extracted_medical_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.dataframe(st.session_state['processed_data'], use_container_width=True)

st.markdown("---")
st.markdown("© 2024 Medical Data Extractor. All rights reserved.")
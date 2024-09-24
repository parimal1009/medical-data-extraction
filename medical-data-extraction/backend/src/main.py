from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
from extractor import extract
import uuid
import os
import pandas as pd

app = FastAPI()

@app.post("/extract_from_doc")
def extract_from_doc(
    file: UploadFile = File(...),
    file_format: str = Form(...)
):
    content = file.file.read()
    UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Generate unique file path
    FILE_PATH = os.path.join(UPLOAD_DIR, str(uuid.uuid4()) + ".pdf")

    with open(FILE_PATH, "wb") as f:
        f.write(content)

    try:
        data = extract(FILE_PATH, file_format)

        # Create a pandas DataFrame from the extracted data
        df = pd.DataFrame([data])

        # Create a unique path for the Excel file
        OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "output")
        excel_file_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.xlsx")

        # Save the DataFrame as an Excel file
        df.to_excel(excel_file_path, index=False)

        # Return the Excel file as a response
        return FileResponse(excel_file_path, filename="extracted_data.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        return {"error": str(e)}

    # finally:
    #     # Clean up the uploaded PDF after extraction
    #     if os.path.exists(FILE_PATH):
    #         os.remove(FILE_PATH)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

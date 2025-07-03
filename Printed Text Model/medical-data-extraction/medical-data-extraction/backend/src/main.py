from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
from extractor import extract
import uuid
import os
import pandas as pd

app = FastAPI()

@app.post("/extract_from_doc")
def extract_from_doc(file: UploadFile = File(...), file_format: str = Form(...)):
    content = file.file.read()

    UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    FILE_PATH = os.path.join(UPLOAD_DIR, str(uuid.uuid4()) + ".png")

    with open(FILE_PATH, "wb") as f:
        f.write(content)

    try:
        data = extract(FILE_PATH, file_format)
        df = pd.DataFrame([data])

        OUTPUT_DIR = os.path.join(os.getcwd(), "output")
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        excel_file_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.xlsx")
        df.to_excel(excel_file_path, index=False)

        return FileResponse(excel_file_path, filename="extracted_data.xlsx",
                            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

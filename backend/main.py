from fastapi import FastAPI, UploadFile, File
from services.ocr_service import extract_text_from_image as extract_text
from services.parser_service import extract_medicines as parse_medicines
import os

# CREATE APP FIRST
app = FastAPI(title="AI Prescription Safety Layer")


@app.get("/")
def root():
    return {"message": "Backend is running successfully"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        temp_file_path = f"temp_{file.filename}"

        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)

        # Run OCR
        raw_text = extract_text(temp_file_path)

        # Delete temp file
        os.remove(temp_file_path)

        if not raw_text:
            return {
                "status": "error",
                "message": "No text detected in image"
            }

        parsed_data = parse_medicines(raw_text)

        return {
            "status": "success",
            "raw_text": raw_text,
            "parsed_data": parsed_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
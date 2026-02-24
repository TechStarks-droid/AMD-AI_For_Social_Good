from fastapi import FastAPI, UploadFile, File
from services.ocr_service import extract_text

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()

    try:
        text = extract_text(contents)
        return {"status": "success", "raw_text": text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

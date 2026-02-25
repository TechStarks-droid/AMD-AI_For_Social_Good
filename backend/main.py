from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from services.ocr_service import extract_text_from_image
from services.parser_service import extract_medicines
from services.mapping_service import map_brands_to_generics
from services.rule_engine import detect_duplicates, check_interactions, calculate_risk
from services.explanation_engine import generate_explanations
from services.myth_service import get_myth_explanation

app = FastAPI(title="AI Prescription Safety Layer")

UPLOAD_FOLDER = "temp_uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.post("/analyze")
async def analyze_prescription(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        raw_text = extract_text_from_image(file_path)
        parsed = extract_medicines(raw_text)
        mapped = map_brands_to_generics(parsed)

        duplicates = detect_duplicates(mapped)
        interactions = check_interactions(mapped)
        risk = calculate_risk(interactions, duplicates)
        explanations = generate_explanations(interactions)

        return JSONResponse(content={
            "medicines": mapped,
            "duplicates": duplicates,
            "interactions": interactions,
            "risk": risk,
            "explanations": explanations
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/myth")
def myth_example():
    return get_myth_explanation("opioids are safe if prescribed")
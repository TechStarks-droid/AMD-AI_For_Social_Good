from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from services.ocr_service import extract_text_from_image
from services.parser_service import extract_medicines
from services.mapping_service import map_brands_to_generics
from services.rule_engine import (
    detect_duplicates,
    check_interactions,
    calculate_risk,
    calculate_coverage
)
from services.explanation_engine import generate_explanations

app = FastAPI(title="AI Prescription Safety Layer")

# Allow frontend access (for local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    return {"message": "AI Prescription Safety Layer API is running."}


@app.post("/analyze")
async def analyze_prescription(file: UploadFile = File(...)):
    try:
        # 1. Save uploaded image temporarily
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. OCR Extraction
        raw_text = extract_text_from_image(file_path)

        # 3. Parse Medicines
        parsed_medicines = extract_medicines(raw_text)

        # 4. Map to Generics
        mapped_medicines = map_brands_to_generics(parsed_medicines)

        # 5. Duplicate Detection
        duplicates = detect_duplicates(mapped_medicines)

        # 6. Interaction Detection
        interactions = check_interactions(mapped_medicines)

        # 7. Risk Calculation
        risk = calculate_risk(interactions, duplicates)

        # 8. Coverage Intelligence
        coverage = calculate_coverage(mapped_medicines)

        # 9. Explanation Layer
        explanations = generate_explanations(interactions)

        return {
            "medicines": mapped_medicines,
            "duplicates": duplicates,
            "interactions": interactions,
            "risk": risk,
            "coverage": coverage,
            "explanations": explanations
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/myth")
def myth_vs_fact():
    return {
        "myth": "If a doctor prescribed it, combining medicines is always safe.",
        "fact": "Even prescribed medicines can interact with each other. Drug interaction checks are important."
    }
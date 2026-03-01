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


def build_interaction_summary(interactions):
    summary = {}

    for interaction in interactions:
        category = interaction["risk_category"]
        severity = interaction["severity"]
        weight = interaction["risk_weight"]

        if category not in summary:
            summary[category] = {
                "total_interactions": 0,
                "severity_distribution": {
                    "high": 0,
                    "moderate": 0,
                    "low": 0
                },
                "total_contribution": 0
            }

        summary[category]["total_interactions"] += 1
        summary[category]["severity_distribution"][severity] += 1
        summary[category]["total_contribution"] += weight

    return summary


@app.post("/analyze")
async def analyze_prescription(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        raw_text = extract_text_from_image(file_path)
        parsed_medicines = extract_medicines(raw_text)
        mapped_medicines = map_brands_to_generics(parsed_medicines)

        duplicates = detect_duplicates(mapped_medicines)
        interactions = check_interactions(mapped_medicines)
        risk = calculate_risk(interactions, duplicates)
        coverage = calculate_coverage(mapped_medicines)

        explanations = generate_explanations(interactions)

        interaction_summary = build_interaction_summary(interactions)

        return {
            "medicines": mapped_medicines,
            "duplicates": duplicates,
            "interactions": interactions,
            "interaction_summary": interaction_summary,
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
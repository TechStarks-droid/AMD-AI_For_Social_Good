import json
import os
from itertools import combinations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DRUG_DB_PATH = os.path.join(BASE_DIR, "..", "knowledge_base", "drugs.json")
INTERACTIONS_DB_PATH = os.path.join(BASE_DIR, "..", "knowledge_base", "interactions.json")

with open(DRUG_DB_PATH) as f:
    DRUG_DB = json.load(f)

with open(INTERACTIONS_DB_PATH) as f:
    INTERACTIONS_DB = json.load(f)


def detect_duplicates(prescription):
    generic_map = {}
    duplicates = []

    for med in prescription:
        for gen in med["generics"]:
            if gen in generic_map:
                duplicates.append({
                    "generic": gen,
                    "drug1": generic_map[gen],
                    "drug2": med["brand"]
                })
            else:
                generic_map[gen] = med["brand"]

    return duplicates


def check_interactions(prescription):
    interactions_found = []
    all_generics = []

    for med in prescription:
        all_generics.extend(med["generics"])

    for drug_a, drug_b in combinations(all_generics, 2):
        for rule in INTERACTIONS_DB:
            if (
                (rule["drug1"] == drug_a and rule["drug2"] == drug_b) or
                (rule["drug1"] == drug_b and rule["drug2"] == drug_a)
            ):
                interactions_found.append(rule)

    return interactions_found


def calculate_risk(interactions, duplicates):
    score = 0
    high = 0
    moderate = 0
    low = 0

    for i in interactions:
        if i["severity"] == "high":
            score += 30
            high += 1
        elif i["severity"] == "moderate":
            score += 15
            moderate += 1
        else:
            score += 5
            low += 1

    duplicate_score = len(duplicates) * 20
    score += duplicate_score

    score = min(score, 100)

    # Risk level classification
    if score <= 19:
        level = "Low"
    elif score <= 49:
        level = "Moderate"
    elif score <= 79:
        level = "High"
    else:
        level = "Critical"

    return {
        "risk_score": score,
        "risk_level": level,
        "severity_breakdown": {
            "high": high,
            "moderate": moderate,
            "low": low,
            "duplicates": len(duplicates)
        }
    }


def calculate_coverage(prescription):
    total = len(prescription)
    unknown = sum(1 for med in prescription if med.get("unknown", False))
    recognized = total - unknown

    if total == 0:
        confidence = "none"
    elif unknown == 0:
        confidence = "complete"
    elif recognized > 0:
        confidence = "partial"
    else:
        confidence = "none"

    return {
        "total_medicines_detected": total,
        "recognized_medicines": recognized,
        "unknown_medicines": unknown,
        "analysis_confidence": confidence,
        "coverage_warning": (
            "Some medicines were not found in the current knowledge base. "
            "Risk analysis may be incomplete."
            if unknown > 0 else None
        )
    }
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
                interactions_found.append({
                    "drug1": rule["drug1"],
                    "drug2": rule["drug2"],
                    "severity": rule["severity"],
                    "mechanism": rule["mechanism"],
                    "risk_category": rule["risk_category"],
                    "risk_weight": rule["risk_weight"]
                })

    return interactions_found


def calculate_risk(interactions, duplicates):
    raw_score = 0

    breakdown = {
        "interaction_contribution": 0,
        "duplicate_contribution": 0,
        "severity_counts": {
            "high": 0,
            "moderate": 0,
            "low": 0
        }
    }

    # Add interaction contributions
    for interaction in interactions:
        weight = interaction["risk_weight"]
        raw_score += weight
        breakdown["interaction_contribution"] += weight
        breakdown["severity_counts"][interaction["severity"]] += 1

    # Add duplicate contribution
    duplicate_score = len(duplicates) * 20
    raw_score += duplicate_score
    breakdown["duplicate_contribution"] = duplicate_score

    # Cap final score
    final_score = min(raw_score, 100)

    # Adjust breakdown if overflow happened
    if raw_score > 100:
        overflow = raw_score - 100
        breakdown["interaction_contribution"] = max(
            breakdown["interaction_contribution"] - overflow, 0
        )

    # Determine risk level
    if final_score <= 19:
        level = "Low"
    elif final_score <= 49:
        level = "Moderate"
    elif final_score <= 79:
        level = "High"
    else:
        level = "Critical"

    return {
        "risk_score": final_score,
        "risk_level": level,
        "breakdown": breakdown
    }


def calculate_coverage(mapped_medicines):
    total = len(mapped_medicines)
    unknown = len([m for m in mapped_medicines if m["unknown"]])
    recognized = total - unknown

    if total == 0:
        confidence = "none"
        warning = "No medicines detected."
    elif unknown == 0:
        confidence = "complete"
        warning = None
    else:
        confidence = "partial"
        warning = "Some medicines were not recognized in the knowledge base."

    return {
        "total_medicines_detected": total,
        "recognized_medicines": recognized,
        "unknown_medicines": unknown,
        "analysis_confidence": confidence,
        "coverage_warning": warning
    }
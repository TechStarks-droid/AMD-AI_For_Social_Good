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
        severity = i["severity"].lower()

        if severity == "high":
            score += 30
            high += 1
        elif severity == "moderate":
            score += 15
            moderate += 1
        elif severity == "low":
            score += 5
            low += 1

    score += len(duplicates) * 20

    return {
        "risk_score": min(score, 100),
        "severity_breakdown": {
            "high": high,
            "moderate": moderate,
            "low": low,
            "duplicates": len(duplicates)
        }
    }
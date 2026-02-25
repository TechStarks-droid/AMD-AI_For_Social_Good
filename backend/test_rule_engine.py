from services.rule_engine import detect_duplicates, check_interactions, calculate_risk

prescription = [
    {"brand": "crocin 650", "generics": ["paracetamol"]},
    {"brand": "calpol 500", "generics": ["paracetamol"]},
    {"brand": "brufen 400", "generics": ["ibuprofen"]},
    {"brand": "warfarin", "generics": ["warfarin"]}
]

duplicates = detect_duplicates(prescription)
interactions = check_interactions(prescription)
result = calculate_risk(interactions, duplicates)

print("\n===== SAFETY REPORT =====")
print("Duplicates:", duplicates)
print("Interactions:", interactions)
print("Final Result:", result)
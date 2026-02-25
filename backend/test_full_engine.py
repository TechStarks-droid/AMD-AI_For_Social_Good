from services.ocr_service import extract_text_from_image
from services.parser_service import extract_medicines
from services.mapping_service import map_brands_to_generics
from services.rule_engine import detect_duplicates, check_interactions, calculate_risk
from services.explanation_engine import generate_explanations

image_path = "sample_prescriptions/sample1.png"

raw_text = extract_text_from_image(image_path)
parsed = extract_medicines(raw_text)
mapped = map_brands_to_generics(parsed)

duplicates = detect_duplicates(mapped)
interactions = check_interactions(mapped)
risk = calculate_risk(interactions, duplicates)

explanations = generate_explanations(interactions)

print("----- FINAL ENGINE OUTPUT -----\n")
print("Mapped:\n", mapped)
print("\nDuplicates:\n", duplicates)
print("\nInteractions:\n", interactions)
print("\nRisk:\n", risk)
print("\nExplanations:\n", explanations)
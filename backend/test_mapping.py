from services.ocr_service import extract_text_from_image
from services.parser_service import extract_medicines
from services.mapping_service import map_brands_to_generics

image_path = "sample_prescriptions/sample1.png"

raw_text = extract_text_from_image(image_path)
parsed = extract_medicines(raw_text)

mapped = map_brands_to_generics(parsed)

print("----- MAPPED OUTPUT -----\n")
print(mapped)
from services.ocr_service import extract_text_from_image
from services.parser_service import extract_medicines

image_path = "sample_prescriptions/sample1.png"

raw_text = extract_text_from_image(image_path)

print("----- RAW OCR TEXT -----\n")
print(raw_text)

print("\n----- STRUCTURED OUTPUT -----\n")

parsed = extract_medicines(raw_text)

print(parsed)
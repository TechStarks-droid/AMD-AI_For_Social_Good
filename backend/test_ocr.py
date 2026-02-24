from services.ocr_service import extract_text_from_image

image_path = "sample_prescriptions/sample1.png"

print("----- RAW OCR OUTPUT -----\n")

text = extract_text_from_image(image_path)

print(text)
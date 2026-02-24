import pytesseract
from PIL import Image
import os


def extract_text_from_image(image_path: str) -> str:
    """
    Extract raw text from prescription image using Tesseract OCR.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    try:
        image = Image.open(image_path)

        # Convert to RGB to avoid format issues
        image = image.convert("RGB")

        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {str(e)}")

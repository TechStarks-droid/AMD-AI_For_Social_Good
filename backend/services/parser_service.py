import re


def extract_medicines(raw_text: str):
    """
    Extract normalized medicine names from raw OCR text.
    Focuses on lines containing 'Rx:'.
    """

    medicines = []

    lines = raw_text.split("\n")

    for line in lines:
        line_clean = line.strip()

        if not line_clean:
            continue

        lower_line = line_clean.lower()

        # Check if line contains 'Rx:'
        if "rx:" in lower_line:
            # Split on 'Rx:' to isolate medicine part
            parts = re.split(r"rx:", line_clean, flags=re.IGNORECASE)

            if len(parts) > 1:
                medicine_part = parts[1].strip()

                # Remove trailing noise like Start Date, SIG, pipes, etc.
                medicine_name = re.split(
                    r"start date|sig:|\|",
                    medicine_part,
                    flags=re.IGNORECASE
                )[0].strip()

                # Remove dosage numbers (anything after first digit)
                medicine_name = re.split(r"\d", medicine_name)[0].strip()

                # Remove common formulation words
                medicine_name = re.split(
                    r"oral|tablet|capsule|extended|release",
                    medicine_name,
                    flags=re.IGNORECASE
                )[0].strip()

                # Final cleanup
                medicine_name = medicine_name.lower().strip()

                if medicine_name:
                    medicines.append({
                        "brand": medicine_name,
                        "dosage": None,
                        "duration": None
                    })

    return medicines
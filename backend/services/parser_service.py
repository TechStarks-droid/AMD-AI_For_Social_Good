import re


def extract_medicines(raw_text: str):
    medicines = []

    lines = raw_text.split("\n")

    for line in lines:
        line_clean = line.strip()

        if not line_clean:
            continue

        lower_line = line_clean.lower()

        if "rx:" in lower_line:
            parts = re.split(r"rx:", line_clean, flags=re.IGNORECASE)

            if len(parts) > 1:
                medicine_part = parts[1].strip()

                medicine_name = re.split(
                    r"start date|sig:|\|",
                    medicine_part,
                    flags=re.IGNORECASE
                )[0].strip()

                # REMOVE DOSAGE NUMBERS
                medicine_name = re.split(r"\d", medicine_name)[0].strip()

                # REMOVE FORMULATION WORDS
                medicine_name = re.split(
                    r"oral|tablet|capsule|extended|release",
                    medicine_name,
                    flags=re.IGNORECASE
                )[0].strip()

                medicine_name = medicine_name.lower().strip()

                if medicine_name and medicine_name not in [m["brand"] for m in medicines]:
                    medicines.append({
                        "brand": medicine_name,
                        "dosage": None,
                        "duration": None
                    })

    return medicines
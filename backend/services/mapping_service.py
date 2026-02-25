import json
import os


def load_knowledge_base():
    base_path = os.path.dirname(os.path.dirname(__file__))
    kb_path = os.path.join(base_path, "knowledge_base", "drugs.json")

    with open(kb_path, "r") as f:
        return json.load(f)


def map_brands_to_generics(parsed_medicines):
    kb = load_knowledge_base()

    generics_data = kb["generics"]
    brands_data = kb["brands"]

    enriched_medicines = []

    for med in parsed_medicines:
        brand = med["brand"]

        if brand not in brands_data:
            # Unknown brand
            enriched_medicines.append({
                "brand": brand,
                "generics": [],
                "classes": [],
                "unknown": True
            })
            continue

        generics = brands_data[brand]

        classes = []
        for generic in generics:
            if generic in generics_data:
                classes.append(generics_data[generic]["class"])

        enriched_medicines.append({
            "brand": brand,
            "generics": generics,
            "classes": list(set(classes)),
            "unknown": False
        })

    return enriched_medicines
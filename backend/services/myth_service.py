MYTHS = {
    "antibiotics cure viral infections": "Antibiotics do not work against viruses. They only treat bacterial infections.",
    "more painkillers means faster relief": "Taking more painkillers than prescribed can cause harm and does not guarantee faster relief.",
    "opioids are safe if prescribed": "Even prescribed opioids carry risks, especially when combined with other sedatives."
}


def get_myth_explanation(myth):
    myth_lower = myth.lower()
    if myth_lower in MYTHS:
        return {
            "myth": myth,
            "fact": MYTHS[myth_lower]
        }
    return {
        "myth": myth,
        "fact": "No verified information available."
    }
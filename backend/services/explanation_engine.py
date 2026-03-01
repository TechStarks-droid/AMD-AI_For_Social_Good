def simplify_interaction(interaction):
    severity = interaction["severity"]
    mechanism = interaction["mechanism"]

    if severity == "high":
        summary = "This combination carries a high safety risk."
    elif severity == "moderate":
        summary = "This combination carries a moderate safety risk."
    else:
        summary = "This combination carries a low safety risk."

    if interaction["risk_category"] == "bleeding":
        risk_type = "It may increase the risk of bleeding."
    elif interaction["risk_category"] == "respiratory_depression":
        risk_type = "It may slow breathing and cause serious breathing problems."
    elif interaction["risk_category"] == "sedation":
        risk_type = "It may cause increased drowsiness and sedation."
    elif interaction["risk_category"] == "hypoglycemia":
        risk_type = "It may lower blood sugar levels excessively."
    else:
        risk_type = "It may increase medication-related risk."

    return {
        "drugs": [interaction["drug1"], interaction["drug2"]],
        "severity": severity,
        "simple_explanation": f"{summary} {risk_type}"
    }


def generate_explanations(interactions):
    explanations = []

    for interaction in interactions:
        explanations.append(simplify_interaction(interaction))

    return explanations
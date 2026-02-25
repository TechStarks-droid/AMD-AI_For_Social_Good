import os
from openai import OpenAI

# Initialize client only if API key exists
client = None
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    client = OpenAI(api_key=api_key)


def fallback_simplification(description):
    """
    Deterministic fallback simplifier.
    Ensures explanations are always simplified,
    even if API fails or quota is exceeded.
    """

    desc = description.lower()

    if "respiratory depression" in desc:
        return "Taking these medicines together can slow breathing and may be dangerous."

    if "sedation" in desc or "drowsiness" in desc:
        return "Using these medicines together can cause extra sleepiness and drowsiness."

    if "bleeding" in desc:
        return "Taking these medicines together may increase the risk of bleeding."

    if "anticoagulant" in desc:
        return "Using these medicines together may increase bleeding risk."

    return "These medicines may not be safe to take together."


def simplify_interaction(interaction):
    """
    Simplifies interaction description using LLM if available.
    Falls back to rule-based simplification if API fails.
    """

    description = interaction["description"]

    # If no API client available, use fallback
    if client is None:
        simplified = fallback_simplification(description)

    else:
        try:
            prompt = f"""
You are a medical safety explanation simplifier.

Rewrite the following interaction explanation in simple, easy-to-understand language.

IMPORTANT RULES:
- Do NOT add medical advice.
- Do NOT suggest treatment.
- Do NOT add new medical facts.
- Only simplify the given explanation.

Original:
{description}

Simple explanation:
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You simplify medical safety explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            simplified = response.choices[0].message.content.strip()

        except Exception:
            # Any API failure → fallback
            simplified = fallback_simplification(description)

    return {
        "drugs": [interaction["drug1"], interaction["drug2"]],
        "severity": interaction["severity"],
        "simple_explanation": simplified
    }


def generate_explanations(interactions):
    """
    Generates simplified explanations
    for all detected interactions.
    """

    explanations = []

    for interaction in interactions:
        explanations.append(simplify_interaction(interaction))

    return explanations
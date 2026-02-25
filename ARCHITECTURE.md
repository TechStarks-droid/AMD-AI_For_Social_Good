AI Prescription Safety Layer
Backend-first prescription safety intelligence engine

System Overview

This project implements a prescription safety intelligence engine designed to analyze printed prescriptions and surface structured safety risks before medication is dispensed or consumed.

It does not provide medical diagnosis.
It does not provide treatment advice.
It does not replace clinical judgment.

The system performs OCR extraction from printed prescriptions, structured medicine parsing, brand-to-generic mapping, duplicate composition detection, drug–drug interaction detection, risk scoring, and controlled explanation generation.

All core safety logic is rule-based and deterministic to ensure transparency, auditability, and reliability.

High-Level Flow

Prescription Image
→ OCR
→ Text Parsing
→ Brand Normalization
→ Generic Mapping
→ Duplicate Detection
→ Interaction Detection
→ Risk Scoring
→ Explanation Layer
→ FastAPI JSON Response

Each layer is isolated and responsible for a single task.

Layer Breakdown

Layer 1 — OCR

File: services/ocr_service.py

This layer uses Tesseract to extract raw text from printed prescriptions.
Handwritten prescriptions are intentionally not supported.

The objective is stable extraction under controlled demo conditions.

Layer 2 — Parsing Engine

File: services/parser_service.py

This layer uses regular expressions to extract medicines from OCR text.
It detects "Rx:" patterns, normalizes brand names, and removes dosage noise.

No NLP model is used. Regex-based parsing ensures predictable behavior and easier debugging.

Layer 3 — Knowledge Base

Files: knowledge_base/drugs.json and knowledge_base/interactions.json

drugs.json contains two structured sections: generics and brands.
Generics include drug class and a base risk level.
Brands map directly to one or more generic compounds.

interactions.json defines known drug–drug interactions with severity levels and structured descriptions.

The database is curated, controlled, and intentionally limited in scope.

Layer 4 — Duplicate Detection

File: services/rule_engine.py

If two medicines share at least one generic compound, they are flagged as duplicate composition.

For example, Crocin and Calpol both contain paracetamol and would be identified as overlapping medication.

Layer 5 — Interaction Engine

This layer performs pairwise comparison of all generics in the prescription.
For every generic A and generic B, the system checks interactions.json.

Supported severities include high, moderate, and low.

The engine is fully rule-based. No predictive modeling or machine learning is used.

Layer 6 — Risk Scoring Engine

The scoring logic assigns weighted values:

High interaction adds 30 points.
Moderate interaction adds 15 points.
Low interaction adds 5 points.
Duplicate composition adds 20 points.

The total score is capped at 100.

Risk levels are interpreted as follows:

0–19 is Low
20–49 is Moderate
50–79 is High
80–100 is Critical

The scoring method is transparent, explainable, and reproducible.

Layer 7 — Explanation Layer

File: services/explanation_engine.py

This layer converts structured interaction descriptions into simplified language.

It does not generate new medical information.
It does not provide treatment advice.
It does not provide diagnosis.

If the OpenAI API is available, it reformats existing interaction descriptions.
If the API is unavailable or quota is exceeded, deterministic fallback logic is used.

The system continues functioning even without external API availability.

Layer 8 — API Layer

File: main.py

Primary endpoint: POST /analyze

The processing pipeline executes the following sequence:

Accept image upload.
Run OCR.
Parse medicines.
Map to generics.
Detect duplicates.
Detect interactions.
Calculate risk score.
Generate explanations.
Return structured JSON response.

Secondary endpoint: GET /myth

This endpoint returns curated myth versus fact clarification.

Design Principles

The architecture is backend-first.
All safety intelligence resides in backend layers.

The safety engine is deterministic and rule-based.

The LLM is strictly contained and used only for language simplification.

The system avoids database dependency and avoids reliance on external APIs for core safety detection.

Scope Control

The system does not support handwritten prescriptions, full pharmaceutical databases, clinical validation, or hospital integration.

Constraints

The prototype was developed in four days.
It uses a curated dataset of approximately 20 to 50 drugs.
It supports printed prescriptions only.
No external drug APIs are integrated.

Conclusion

This system demonstrates layered backend architecture, deterministic safety detection, transparent risk scoring, controlled LLM integration, and resilient fallback handling.

It operates as a prescription safety intelligence layer rather than a conversational chatbot.
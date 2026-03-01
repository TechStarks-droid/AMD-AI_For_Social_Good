AI Prescription Safety Layer
========
A backend-first prescription safety intelligence engine built to detect medication risks from printed prescriptions.

Overview
========
Medication errors and drug interactions remain a significant safety issue, especially when multiple drugs are prescribed together.

This project implements a structured safety engine that analyzes printed prescriptions and identifies:

Duplicate drug compositions
Known drug–drug interactions
Risk severity levels
Simplified safety explanations

The system is not a chatbot and does not provide diagnosis or treatment advice.
It operates as a deterministic safety layer designed to surface structured risk signals.

Core Capabilities
========
The engine performs the following pipeline:

Image upload of printed prescription
OCR extraction using Tesseract
Regex-based medicine parsing
Brand-to-generic mapping
Duplicate composition detection
Drug–drug interaction detection
Weighted risk scoring
Controlled explanation generation with fallback handling

All safety logic is rule-based and transparent.

Architecture Approach
========
The system is designed with clear backend layering.

OCR layer extracts raw text.
Parsing layer structures medicine information.
Knowledge base layer maps brands to generics.
Rule engine detects duplicates and interactions.
Risk engine assigns a score between 0 and 100.
Explanation layer reformats structured interaction data.
FastAPI exposes the engine through a single /analyze endpoint.

The LLM component is strictly contained and used only for language simplification.
Core safety detection does not depend on any external API.

Example Output

The API returns structured JSON including:

Mapped medicines
Detected duplicates
Detected interactions with severity
Numerical risk score
Risk level classification
Simplified explanations

The output is explainable and reproducible.

Design Philosophy
========
The system follows four principles:

Deterministic safety logic
Backend-first architecture
Strict LLM containment
Demo reliability under constrained conditions

The engine avoids unnecessary infrastructure such as database orchestration or external pharmaceutical APIs to maintain clarity and stability within a four-day prototype build.

Scope
========
This prototype supports printed prescriptions only.
Handwritten prescriptions are intentionally excluded.
The knowledge base is curated and limited to a focused drug set.
The system does not claim clinical validation.

Technology Stack
========
Backend: FastAPI

OCR: Tesseract

Data: JSON-based knowledge base

LLM: OpenAI API with deterministic fallback

Language: Python

How to Run
========
Install dependencies from requirements.txt

Ensure Tesseract is installed and available in PATH

Run the FastAPI server

Access the /analyze endpoint via Swagger UI

Conclusion
========
AI Prescription Safety Layer demonstrates how a structured, rule-based backend system can surface medication safety risks in a transparent and controlled manner.

It is designed as a safety intelligence layer, not as a conversational assistant.

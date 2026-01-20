# Receipt Survey Bot

A Python-based automation system that extracts structured data from receipt images using OCR and programmatically completes multi-step web forms via browser automation. This project is designed as a technical proof-of-concept demonstrating OCR pipelines, data parsing, and reliable end-to-end automation workflows.

---

## Features
- Optical Character Recognition (OCR) for receipt text extraction
- Structured parsing of dates, amounts, and identifiers
- Automated multi-step form interaction using browser automation
- Modular design for OCR, parsing, and form submission logic
- Debug tooling for OCR accuracy analysis

---

## Project Structure
receipt-survey-bot/
├── extract_receipt_info.py
├── ocr.py
├── ocr_debug.py
├── survey_filler.py
├── main.py
├── .gitignore
├── README.md

---

## Requirements
- Python 3.10+
- Virtual environment recommended
- OCR engine (e.g., Tesseract) installed locally
- Playwright-compatible browser

---

## Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install

---

## Usage
python main.py

The system processes a receipt image using OCR, extracts relevant structured fields, and uses the extracted data to complete a web form automatically.

---

## Notes
- Receipt images, browser state, and environment variables are intentionally excluded from version control.
- This repository focuses on automation techniques and system design rather than deployment at scale.
- Intended for educational and demonstration purposes only.

---

## Key Technical Concepts Demonstrated
- OCR data normalization and error handling
- Deterministic parsing of semi-structured text
- Browser automation reliability (timing, selectors, retries)
- Separation of concerns across pipeline stages

---

## Disclaimer
This project is provided for educational and technical demonstration purposes only. Users are responsible for ensuring compliance with all applicable terms of service and policies when adapting automation workflows to real-world systems.

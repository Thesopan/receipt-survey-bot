from ocr import read_receipt
from extract_receipt_info import extract_info_from_text
from survey_filler import run_survey

receipt_path = "IMG_6878.jpg"
text, _ = read_receipt(receipt_path)

print("\n=== RAW OCR OUTPUT ===")
print(text)

print("\n=== DEBUG: Store Line Candidates ===")
for line in text.splitlines():
    if "store" in line.lower():
        print(f">>> {line}")

info = extract_info_from_text(text)

print("\n📌 Extracted Info:")
print(info)

if info["store"] and info["date"] and info["hour"] and info["minute"]:
    run_survey(info["store"], info["date"], info["hour"], info["minute"])
else:
    print("❌ Incomplete receipt info — not filling survey.")

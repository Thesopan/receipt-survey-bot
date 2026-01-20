import re
from datetime import datetime

def extract_info_from_text(raw_text, word_list=None):
    store_number = None
    date = None
    hour = None
    minute = None

    # Clean up weird characters
    cleaned_text = raw_text.replace("|", ":").replace(";", ":").replace("—", "-").replace("–", "-")

    # === 1. Extract store number (fuzzy match "store" as "tore")
    lines = cleaned_text.splitlines()
    for i, line in enumerate(lines):
        line_clean = line.strip().lower()
        if "tore" in line_clean:  # fuzzy match for store
            match = re.search(r"\b\d{4,6}\b", line_clean)
            if match:
                store_number = match.group(0)
                print(f"📎 Store line (fuzzy): {line}")
                break
            # fallback: look on next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                match = re.search(r"\b\d{4,6}\b", next_line)
                if match:
                    store_number = match.group(0)
                    print(f"📎 Store (from next line): {next_line}")
                    break

    # === 2. Extract MM/DD/YYYY date
    date_match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", cleaned_text)
    if date_match:
        date = date_match.group(0)
    else:
        alt = re.search(r"(\d{1,2})[- ]([A-Za-z]{3})[- ](\d{4})", cleaned_text)
        if alt:
            day, mon, year = alt.groups()
            try:
                date = datetime.strptime(f"{day}-{mon}-{year}", "%d-%b-%Y").strftime("%m/%d/%Y")
            except:
                pass

    # === 3. Extract HH:MM:SS time
    time_match = re.search(r"(\d{1,2}):(\d{2}):\d{2}", cleaned_text)
    if time_match:
        hour = time_match.group(1).zfill(2)
        minute = time_match.group(2).zfill(2)

    return {
        "store": store_number,
        "date": date,
        "hour": hour,
        "minute": minute
    }

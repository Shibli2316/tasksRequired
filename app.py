"""
process_meds.py

Load prescriptions.csv, parse medication text into structured fields,
and save prescriptions_clean.csv.

"""
# importing regular expressions and pandas for data manipulation and pathlib for file path handling
import re
import pandas as pd
from pathlib import Path

# Input/Output paths. It should be in the same folder as this script.
IN_PATH = Path("prescriptions.csv")
OUT_PATH = Path("prescriptions_clean.csv")

# Lookup table to normalize drug names
INGREDIENT_MAPPING = {
    "ibu": "Ibuprofen",
    "ibuprofen": "Ibuprofen",
    "amoxicillin": "Amoxicillin",
    "aspirin": "Aspirin",
    "metformin-ratiopharm": "Metformin",
    "metformin": "Metformin",
    "l-thyroxin": "L-Thyroxin",
    "lthyroxin": "L-Thyroxin",
    "diclofenac": "Diclofenac",
}

# skip dosage parsing for these
TOPICAL_TERMS = {"gel", "cream", "ointment", "spray", "patch", "lotion", "solution"}


# The functions below parse and standardize the medication text field. removes any text in parentheses.
def remove_parentheses(text: str) -> str:
    return re.sub(r"\(.*?\)", "", text)


# Replaces multiple whitespace characters with a single space and trims leading/trailing spaces.
def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()



# Detect if the medication is topical based on keywords.
def detect_topical(text: str) -> bool:
    return any(term in text.lower() for term in TOPICAL_TERMS)



# Standardizes the active ingredient name from the medication text.
def standardize_active_ingredient(text: str) -> str:
    t = remove_parentheses(text)
    t = normalize_whitespace(t)
    # Remove dosage tokens
    t = re.sub(r"\b\d+(?:[.,]\d+)?\s*(mg|g|microgram|mcg|ug|µg)?\b", "", t, flags=re.IGNORECASE)
    # Remove common suffixes
    t = re.sub(r"\b(filmtabletten|film|tabletten|tube|tab|caps?|retard|sr|dragee)\b", "", t, flags=re.IGNORECASE)
    t = t.replace("-", " ")
    t = normalize_whitespace(t)

    tokens = t.split()
    if not tokens:
        return None
    candidate = tokens[0].lower()
    if len(tokens) > 1 and len(tokens[0]) <= 2:
        candidate = f"{tokens[0].lower()}-{tokens[1].lower()}"
    candidate = candidate.strip(",. ")

    # Map to standardized name
    if candidate in INGREDIENT_MAPPING:
        return INGREDIENT_MAPPING[candidate]
    return candidate.replace("-", " ").title()





# Extracts dosage and unit from the medication text.
def extract_dosage_and_unit(text: str):
    if detect_topical(text):
        return (None, None)
    pattern = re.compile(r"(?P<dos>\d+(?:[.,]\d+)?)\s*(?P<unit>mg|g|microgram|mcg|ug|µg)?\b", flags=re.IGNORECASE)
    m = pattern.search(text)
    if not m:
        return (None, None)
    dos = m.group("dos").replace(",", ".")
    unit = m.group("unit")
    if unit:
        unit_low = unit.lower()
        if unit_low in {"mcg", "ug", "µg"}:
            unit_std = "microgram"
        elif unit_low == "micrograms":
            unit_std = "microgram"
        else:
            unit_std = unit_low
    else:
        # Default to mg if number given but no unit
        unit_std = "mg"
    return (dos, unit_std)

def main():
    df = pd.read_csv(IN_PATH, dtype=str)

    # Standardize dates
    df["prescription_date"] = pd.to_datetime(df["prescription_date"], errors="coerce").dt.strftime("%Y-%m-%d")


# Parse medication text into structured fields 
    active, dosages, units = [], [], []
    for txt in df["medication_text"].fillna(""):
        ai = standardize_active_ingredient(txt)
        dos, unit = extract_dosage_and_unit(txt)
        active.append(ai)
        dosages.append(dos)
        units.append(unit)

    df["active_ingredient"] = active
    df["dosage"] = dosages
    df["unit"] = units

    df.to_csv(OUT_PATH, index=False)
    print(f"Processed {len(df)} rows. Output saved to {OUT_PATH}")

if __name__ == "__main__":
    main()
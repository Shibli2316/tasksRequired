# process_meds.py

A Python script to clean and normalize prescription data from a CSV file.  
It extracts active ingredients, dosage, and units from raw medication text, standardizes drug names, detects topical medications, and outputs a cleaned dataset.

---

## Features

- Reads prescriptions from **`prescriptions.csv`**
- Standardizes drug names using a lookup mapping  
  - e.g., `"ibu"` → `"Ibuprofen"`
- Cleans packaging/form terms like `"filmtabletten"`, `"caps"`, etc.
- Detects **topical medications** (gel, cream, ointment, spray, etc.) and skips dosage parsing for them
- Extracts dosage and standardizes units (`mg`, `g`, `microgram`)
- Normalizes prescription dates into **YYYY-MM-DD** format
- Saves processed output to **`prescriptions_clean.csv`**

---

## Requirements

- Python **3.8+**
- Dependencies:
  - [pandas](https://pandas.pydata.org)

Install dependencies with: pip install pandas


---

## Input File Format

The script expects a CSV file named **`prescriptions.csv`** in the same directory, containing (at minimum):

- `prescription_date` — date of prescription (any common format, e.g. `12/03/2021`)
- `medication_text` — raw string of the medication description

**Example input (`prescriptions.csv`):**




---

## Output File Format

The cleaned data will be written to **`prescriptions_clean.csv`**, including structured fields:

- `active_ingredient`
- `dosage`
- `unit`

**Example output (`prescriptions_clean.csv`):**




---

## Usage

Run the script from the command line: python process_meds.py


This will:
1. Load `prescriptions.csv`
2. Parse, clean, and structure the medication text
3. Save results to `prescriptions_clean.csv`
4. Print a summary of processed rows

---

## How It Works

- **Drug name normalization** uses a dictionary to standardize names  
- **Regex parsing** extracts numeric dosage and unit values  
- **Topical detection** skips dosage parsing for creams, gels, sprays, etc.  
- **Date formatting** ensures consistent YYYY-MM-DD format  

---








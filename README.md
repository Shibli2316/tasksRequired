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
| prescription_date | medication_text                  |
|-------------------|----------------------------------|
| 2021-03-12        | Ibuprofen 400mg Filmtabletten    |
| 2021-04-01        | Amoxicillin 500 mg Capsules      |
| 2021-04-10        | Diclofenac Gel 120 gm            |
| 2021-05-05        | Metformin-ratiopharm 850mg       |




---

## Output File Format

The cleaned data will be written to **`prescriptions_clean.csv`**, including structured fields:

- `active_ingredient`
- `dosage`
- `unit`

**Example output (`prescriptions_clean.csv`):**
| prescription_date | medication_text                  | active_ingredient | dosage | unit |
|-------------------|----------------------------------|-------------------|--------|------|
| 2021-03-12        | Ibuprofen 400mg Filmtabletten    | Ibuprofen         | 400    | mg   |
| 2021-04-01        | Amoxicillin 500 mg Capsules      | Amoxicillin       | 500    | mg   |
| 2021-04-10        | Diclofenac Gel Tube              | Diclofenac        |        |      |
| 2021-05-05        | Metformin-ratiopharm 850mg       | Metformin         | 850    | mg   |




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



## Answer to Bonus Question 
Indeed the rule based system that i have designed may work efficiently with less or limited data but once the data starts to exceed human expectations (millions or billions of data points) the script will most likely break as python in itself have many limitations with large dataset. I may choose to switch over to spark for handling real time large dataset but when it comes to LLM’s like Gemini or ChatGPT leveraging their power will be a huge step as they are trained with unprecedented datasets that includes the knowledge about all the medical chemicals and names that even a doctor may not be well aware of and that too from all around the world. It can very easily handle the misspelled data (unlike this script) it can also help in define the medication based on past knowledge and current situation. And help in understanding patterns that are unseen or seen better. 
<br>
But since any LLM with sufficient data can halucinate or simply make up answers it is important to keep it in check and to do so we would need to make a structured prompt or API interface where we can pass the dosage and it would identify ingredient, dosage units etc. We can easily leverage the power of transfer learning into this as the LLM is already trained in a general and larger dataset we can just train it into our smaller dataset. It will reduce the cost and time it would need to train a complete LLM and it will benefit us for the specific task we need. This might be done by providing a few annotated examples and asking the model to extract the relevant fields for each prescription entry. The LLM could be used in a batch processing pipeline, integrating with existing data cleaning steps or as an augmentation to flag cases with uncertainty for human review.
<br>
Main challenges: cost, latency, and reliability. API calls cost money and latency increases by caching every resolved medication string and batching many examples into one call. We can also use a lookup database (RxNorm / local pharmacopeia) to confirm or replace the LLM's candidate mapping. Another major challenge as already mentioned  is hallucination: LLMs may invent doses or codes if not constrained. To overcome this i propose the following solutions
1. forcing structured outputs with validation rules, 
2. falling back to rule-based parsing when the model's confidence is low, and 
3. adding a human-in-the-loop review for low-confidence or high-impact records. For highly sensitive clinical data, consider an on-prem or private LLM (or de-identified inputs) to satisfy privacy/regulatory requirements.

<br>
To implement it we need:
<br>
1. good prompt engineering with exact specifications  Example final-instruction: “Return only JSON with keys: active_ingredient, dosage, unit, form, confidence (0–1). If no dosage, set dosage=null and unit=null.” <br>
2. Validation so that it dosent make a mistake including a human if needed, so that the dosage remain in limit and it dosent go beyond the range checks.<br>
3. And for precision a temperature of 0





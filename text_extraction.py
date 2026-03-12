import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# OCR function
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Example usage
text = extract_text_from_image(r"images\interaction\prescription_2.png")

from rapidfuzz import process

# Example medicine list
medicine_list =  [
    "Aspirin", "Paracetamol", "Crocin", "Dolo", "Dolo 650",
    "Metformin", "Glycomet",
    "Atorvastatin", "Atorva", "Atorlip", "Rosuvastatin", "Simvastatin",
    "Ibuprofen", "Brufen", "Combiflam", "Naproxen", "Diclofenac",
    "Tramadol", "Morphine",
    "Amlodipine", "Amlong",
    "Losartan", "Losar", "Telmisartan", "Olmesartan",
    "Bisoprolol", "Atenolol", "Metoprolol", "Propranolol",
    "Hydrochlorothiazide", "Furosemide", "Spironolactone",
    "Digoxin", "Nitroglycerin", "Isosorbide Mononitrate",
    "Pantoprazole", "Pantocid", "Rabeprazole", "Esomeprazole",
    "Ranitidine", "Sucralfate",
    "Ondansetron", "Domperidone", "Metoclopramide",
    "Amoxicillin", "Cefixime", "Azithromycin", "Ciprofloxacin",
    "Clarithromycin", "Doxycycline", "Cloxacillin", "Ampicillin",
    "Metronidazole", "Tinidazole", "Nitrofurantoin",
    "Fluconazole", "Itraconazole", "Ketoconazole",
    "Acyclovir", "Valacyclovir", "Oseltamivir",
    "Rifampicin", "Isoniazid", "Ethambutol", "Pyrazinamide",
    "Linezolid", "Vancomycin", "Gentamicin", "Amikacin",
    "Ceftriaxone", "Piperacillin-Tazobactam", "Meropenem",
    "Levothyroxine",
    "Insulin", "Insulin Human Actrapid", "Insulin Glargine",
    "Glimepiride", "Gliclazide", "Pioglitazone",
    "Sitagliptin", "Vildagliptin", "Dapagliflozin",
    "Clopidogrel", "Warfarin", "Heparin", "Enoxaparin",
    "Salbutamol", "Formoterol", "Budesonide", "Montelukast",
    "Cetirizine", "Levocetirizine", "Fexofenadine",
    "Chlorpheniramine", "Diphenhydramine"
]

def extract_medicines(text, medicine_list):
    found = []
    for word in text.split():
        match = process.extractOne(word, medicine_list, score_cutoff=80)
        if match:
            found.append(match[0])
    return list(set(found))

# Example usage
medicines = extract_medicines(text, medicine_list)
print("Medicines found:", medicines)
import pandas as pd
from itertools import combinations

def check_drug_interactions(medicine_list, csv_path):
    # Load drug interaction CSV
    df = pd.read_csv(csv_path)

    # Normalize drug names (lowercase for matching)
    df['drug1_normalized'] = df['drug1_normalized'].str.lower()
    df['drug2_normalized'] = df['drug2_normalized'].str.lower()
    df['severity'] = df['severity'].astype(str)

    # Prepare medicine list
    meds = [m.lower() for m in medicine_list]

    # Generate all possible pairs from prescription
    pairs = list(combinations(meds, 2))

    # Check interactions
    # Check interactions based on your CSV structure
    warnings = []
    for d1, d2 in pairs:
     match = df[
        ((df['drug1_normalized'] == d1) & (df['drug2_normalized'] == d2)) |
        ((df['drug1_normalized'] == d2) & (df['drug2_normalized'] == d1))
    ]
    if not match.empty:
        for _, row in match.iterrows():
            warnings.append(
                f"⚠️ Interaction between {row['drug1_normalized']} and {row['drug2_normalized']} "
                f"(Severity: {row['severity']}): {row['description']} [Source: {row['reference']}]"
            )

    return warnings

# Example usage
medicine_list =  [
    "Aspirin", "Paracetamol", "Crocin", "Dolo", "Dolo 650",
    "Metformin", "Glycomet",
    "Atorvastatin", "Atorva", "Atorlip", "Rosuvastatin", "Simvastatin",
    "Ibuprofen", "Brufen", "Combiflam", "Naproxen", "Diclofenac",
    "Tramadol", "Morphine",
    "Amlodipine", "Amlong",
    "Losartan", "Losar", "Telmisartan", "Olmesartan",
    "Bisoprolol", "Atenolol", "Metoprolol", "Propranolol",
    "Hydrochlorothiazide", "Furosemide", "Spironolactone",
    "Digoxin", "Nitroglycerin", "Isosorbide Mononitrate",
    "Pantoprazole", "Pantocid", "Rabeprazole", "Esomeprazole",
    "Ranitidine", "Sucralfate",
    "Ondansetron", "Domperidone", "Metoclopramide",
    "Amoxicillin", "Cefixime", "Azithromycin", "Ciprofloxacin",
    "Clarithromycin", "Doxycycline", "Cloxacillin", "Ampicillin",
    "Metronidazole", "Tinidazole", "Nitrofurantoin",
    "Fluconazole", "Itraconazole", "Ketoconazole",
    "Acyclovir", "Valacyclovir", "Oseltamivir",
    "Rifampicin", "Isoniazid", "Ethambutol", "Pyrazinamide",
    "Linezolid", "Vancomycin", "Gentamicin", "Amikacin",
    "Ceftriaxone", "Piperacillin-Tazobactam", "Meropenem",
    "Levothyroxine",
    "Insulin", "Insulin Human Actrapid", "Insulin Glargine",
    "Glimepiride", "Gliclazide", "Pioglitazone",
    "Sitagliptin", "Vildagliptin", "Dapagliflozin",
    "Clopidogrel", "Warfarin", "Heparin", "Enoxaparin",
    "Salbutamol", "Formoterol", "Budesonide", "Montelukast",
    "Cetirizine", "Levocetirizine", "Fexofenadine",
    "Chlorpheniramine", "Diphenhydramine"
]
csv_path = r"C:\Users\user\Documents\blister images\project\interactions.csv"

results = check_drug_interactions(medicine_list, csv_path)
for r in results:
    print(r)
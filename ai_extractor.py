import spacy
from rapidfuzz import process

nlp = spacy.load("medicine_model")

# From your text_extraction.py
medicine_list = ["Aspirin", "Paracetamol", "Crocin", "Dolo", "Dolo 650",
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
    "Chlorpheniramine", "Diphenhydramine"]  # Paste your full list here

def extract_medicines(text):
    doc = nlp(text)
    candidates = [ent.text.title() for ent in doc.ents if ent.label_ == "MEDICINE"]
    medicines = []
    for cand in candidates:
        match = process.extractOne(cand.lower(), [m.lower() for m in medicine_list], score_cutoff=80)
        if match:
            medicines.append(match[0].title())
    return list(set(medicines))  # Dedupe
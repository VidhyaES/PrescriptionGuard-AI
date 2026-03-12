import json
import pandas as pd
import random

# Load interaction database
df = pd.read_csv("data/interactions.csv")

# Normalize for safety
df["drug1_normalized"] = df["drug1_normalized"].str.title()
df["drug2_normalized"] = df["drug2_normalized"].str.title()

# Expanded medicine list (from your text_extraction.py)
medicine_list = [
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

# Templates for realistic prescriptions
templates = [
    "Happy Clinic\nDr. Sample, MBBS, MD\n123 Medical Street, City, State, ZIP\nPhone: +91 {phone} | Reg No: {reg}\nName: {name} ID: {pid}\nAge: {age} Gender: {gender}\nContact: {contact}\nDate: {date}\nMEDICATIONS\nMedicine Frequency Duration\n{med1} {freq1} {dur1}\n{med2} {freq2} {dur2}\nSignature:\nDr. Sample, MBBS, MD",
    "Patient: {name}, Age: {age}\nPrescribed: {med1} daily, {med2} as needed.\nNotes: Avoid alcohol.\nDoctor: Dr. Sample",
    "{med1} and {med2} once daily after food.\nClinic: Happy Clinic\nDate: {date}"
]

frequencies = ["Once daily", "Twice daily", "Before food", "After food"]
durations = ["7 days", "14 days", "Ongoing"]
genders = ["Male", "Female"]
phones = ["1234567890", "9876543210"]
regs = ["REG123", "REG456"]
names = ["John Doe", "Jane Smith", "Kannan"]
pids = ["PID001", "PID002"]
ages = ["30", "45", "61"]
contacts = ["9688616487", "5551234"]
dates = ["09-02-2026", "10-02-2026"]

# Generate diverse sentences
sentences = []
for _ in range(1000):  # Larger dataset
    template = random.choice(templates)
    med_pair = random.sample(medicine_list, 2)
    sentence = template.format(
        phone=random.choice(phones), reg=random.choice(regs), name=random.choice(names),
        pid=random.choice(pids), age=random.choice(ages), gender=random.choice(genders),
        contact=random.choice(contacts), date=random.choice(dates),
        med1=med_pair[0], med2=med_pair[1],
        freq1=random.choice(frequencies), freq2=random.choice(frequencies),
        dur1=random.choice(durations), dur2=random.choice(durations)
    )
    sentences.append(sentence)

# Save raw text
with open("interaction_prescriptions.txt", "w") as f:
    f.write("\n".join(sentences))

# Create NER training data (with hold-out for eval)
def create_training_data(text_lines):
    data = []
    for line in text_lines:
        line_lower = line.lower()
        entities = []
        used_spans = []
        for med in medicine_list:
            med_lower = med.lower()
            start = line_lower.find(med_lower)
            while start != -1:
                end = start + len(med)
                overlap = any(not (end <= s or start >= e) for s, e, _ in used_spans)
                if not overlap:
                    entities.append((start, end, "MEDICINE"))
                    used_spans.append((start, end, "MEDICINE"))
                start = line_lower.find(med_lower, end)
        if entities:
            data.append((line, {"entities": sorted(entities)}))
    return data

full_data = create_training_data(sentences)
random.shuffle(full_data)
train_data = full_data[:800]
eval_data = full_data[800:]

with open("interaction_train_data.json", "w") as f:
    json.dump(train_data, f, indent=4)

with open("interaction_eval_data.json", "w") as f:
    json.dump(eval_data, f, indent=4)

print("✅ Diverse interaction-based dataset created (800 train, 200 eval)")
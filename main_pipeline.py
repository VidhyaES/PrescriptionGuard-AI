from ocr import extract_text
from ai_extractor import extract_medicines
from interaction_checker import check_interactions

IMAGE_PATH = r"prescriptions\prescription_issues_43.png"
CSV_PATH = r"data\interactions.csv"

print("\n--- AI POWERED PRESCRIPTION ANALYSIS SYSTEM ---\n")

# Step 1: OCR
text = extract_text(IMAGE_PATH)
print("Extracted Text:\n", text)

# Step 2: AI Medicine Extraction
medicines = extract_medicines(text)
print("\nDetected Medicines:")
for med in medicines:
    print(" -", med)

# Step 3: Drug Interaction Detection (focus on dangerous)
warnings = check_interactions(medicines, CSV_PATH, severity_threshold="major")

print("\nDrug Interaction Report:")
if warnings:
    for w in warnings:
        print(w)
else:
    print("No dangerous drug interactions detected.")

print("\n--- Analysis Completed Successfully ---")
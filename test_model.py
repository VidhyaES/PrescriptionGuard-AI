import spacy

nlp = spacy.load("medicine_model")

text = "Patient prescribed Paracetamol and Dolo 650"

doc = nlp(text)

print("Detected Medicines:")
for ent in doc.ents:
    print(ent.text, ent.label_)
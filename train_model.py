import spacy
import json
from spacy.training.example import Example

# Create blank English model
nlp = spacy.blank("en")

# Add NER pipeline
ner = nlp.add_pipe("ner")
ner.add_label("MEDICINE")

# Load training data
with open("interaction_train_data.json") as f:
    TRAIN_DATA = json.load(f)

# Initialize optimizer
optimizer = nlp.initialize()

print("Starting training...")

for epoch in range(50):
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], sgd=optimizer, losses=losses, drop=0.4)
    
    print(f"Epoch {epoch+1}/50 - Loss: {losses.get('ner', 0.0):.4f}")

# Save the trained model
nlp.to_disk("medicine_model")

print("✅ Model trained and saved successfully!")
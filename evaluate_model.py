import spacy
import json
from spacy.scorer import Scorer
from spacy.training.example import Example

nlp = spacy.load("medicine_model")

with open("interaction_eval_data.json") as f:
    EVAL_DATA = json.load(f)

scorer = Scorer()
examples = []
for text, annotations in EVAL_DATA:
    doc = nlp(text)
    example = Example.from_dict(doc, annotations)
    examples.append(example)

scores = scorer.score(examples)
print("Evaluation Metrics:")
print(f"Precision: {scores['ents_p']:.3f}")
print(f"Recall: {scores['ents_r']:.3f}")
print(f"F1-Score: {scores['ents_f']:.3f}")
print("Per-Entity Metrics:")
print(scores['ents_per_type'])
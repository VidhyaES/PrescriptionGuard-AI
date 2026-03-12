# 💊 PrescriptionGuard-AI

> AI-powered prescription analysis system that extracts medicines from prescription images using OCR and automatically flags dangerous drug interactions.


---

## 🔍 What It Does

PrescriptionGuard-AI is a 3-stage pipeline:

1. **OCR Extraction** — Reads a prescription image and extracts raw text using Tesseract OCR
2. **AI Medicine Detection** — Uses an NLP-based extractor to identify medicine names from the text
3. **Drug Interaction Check** — Cross-references detected medicines against a curated interaction database and flags dangerous (major) interactions

---

## 🖥️ Demo

Upload a prescription image → get a structured report of detected medicines and any dangerous drug interactions — all in seconds.

---

## 🗂️ Project Structure

```
PrescriptionGuard-AI/
│
├── app.py                    # Flask web application
├── main_pipeline.py          # CLI pipeline (OCR → Extract → Check)
├── ocr.py                    # Tesseract OCR wrapper
├── ai_extractor.py           # AI-based medicine name extractor
├── interaction_checker.py    # Drug interaction detection logic
├── text_extraction.py        # Text preprocessing utilities
│
├── train_model.py            # Model training script
├── evaluate_model.py         # Model evaluation script
├── test_model.py             # Model testing script
├── dataset_generator.py      # Training dataset generation
│
├── data/
│   └── interactions.csv      # Drug interaction database
│
├── prescriptions/            # Sample prescription images
├── templates/                # HTML templates (Flask)
│   ├── index.html            # Landing page
│   ├── analyze.html          # Upload page
│   └── result.html           # Results page
│
├── interaction_train_data.json
├── interaction_eval_data.json
└── interaction_prescriptions.txt
```

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/VidhyaES/PrescriptionGuard-AI.git
cd PrescriptionGuard-AI

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

---

## 🚀 Usage

### Web App (Flask)
```bash
python app.py
```
Then open `http://localhost:5000` in your browser, upload a prescription image, and get instant results.

### CLI Pipeline
```bash
python main_pipeline.py
```
Edit `IMAGE_PATH` in `main_pipeline.py` to point to your prescription image.

---

## 📊 Pipeline Output Example

```
--- AI POWERED PRESCRIPTION ANALYSIS SYSTEM ---

Extracted Text:
 Metformin 500mg, Warfarin 5mg, Aspirin 100mg...

Detected Medicines:
 - Metformin
 - Warfarin
 - Aspirin

Drug Interaction Report:
 ⚠️  MAJOR: Warfarin + Aspirin — Increased bleeding risk

--- Analysis Completed Successfully ---
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Flask |
| OCR Engine | Tesseract / pytesseract |
| Medicine Extraction | NLP / AI-based extractor |
| Interaction Database | Custom CSV |
| Frontend | HTML, CSS, Jinja2 |

---

## 📁 Dataset

The interaction database (`data/interactions.csv`) contains drug pairs with severity levels (`minor`, `moderate`, `major`). The system filters for **major** interactions by default to minimize false alarms while catching dangerous combinations.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Vidhya E S**  
AI/ML & Computer Vision Developer  
🔗 [Portfolio](https://vidhya-es-portfolio.vercel.app/) | [GitHub](https://github.com/VidhyaES)

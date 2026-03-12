from flask import Flask, request, render_template
import os
from ocr import extract_text
from ai_extractor import extract_medicines
from interaction_checker import check_interactions

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

CSV_PATH = "data/interactions.csv"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# ====================== NEW ROUTES ======================
@app.route('/')
def landing():
    return render_template('index.html')      # ← Beautiful landing page

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')    # ← Your working upload page

# ====================== ORIGINAL UPLOAD LOGIC (unchanged) ======================
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('analyze.html', error="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('analyze.html', error="No selected file")
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        try:
            text = extract_text(filepath)
            medicines = extract_medicines(text)
            warnings = check_interactions(medicines, CSV_PATH, severity_threshold="major")
        except Exception as e:
            os.remove(filepath)
            return render_template('analyze.html', error=f"Processing error: {str(e)}")
        
        os.remove(filepath)
        return render_template('result.html', text=text, medicines=medicines, warnings=warnings)
    
    return render_template('analyze.html', error="Invalid file type")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from medicines import get_random_medicines
from patients import get_random_patient  # Assuming you have this; if not, add randomization below

OUTPUT_DIR = "prescriptions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Image dimensions (A4-like at 72 DPI for simplicity; scale up for higher res)
WIDTH, HEIGHT = 595, 842  # A4 in points (approx pixels at 72 DPI)
BG_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
BLUE_COLOR = (79, 129, 189)  # Hex #4F81BD for table header
LINE_COLOR = (0, 0, 255)  # Blue for lines

# Fonts (use system defaults; install Arial/Helvetica if needed)
try:
    TITLE_FONT = ImageFont.truetype("arialbd.ttf", 24)  # Bold for title
    BOLD_FONT = ImageFont.truetype("arialbd.ttf", 12)
    NORMAL_FONT = ImageFont.truetype("arial.ttf", 12)
except IOError:
    TITLE_FONT = ImageFont.load_default()  # Fallback
    BOLD_FONT = ImageFont.load_default()
    NORMAL_FONT = ImageFont.load_default()

def draw_text(draw, text, x, y, font=NORMAL_FONT, color=TEXT_COLOR):
    draw.text((x, y), text, font=font, fill=color)

def draw_line(draw, start, end, color=LINE_COLOR, width=1):
    draw.line([start, end], fill=color, width=width)

def draw_rectangle(draw, coords, fill=None, outline=LINE_COLOR, width=1):
    draw.rectangle(coords, fill=fill, outline=outline, width=width)

def generate_prescription(index):
    patient = get_random_patient()
    medicines = get_random_medicines()
    date = datetime.now().strftime('%d-%m-%Y')

    file_path = f"{OUTPUT_DIR}/prescription_issues_{index}.png"

    # Create image
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Header
    draw_text(draw, "Happy Clinic", 200, 40, TITLE_FONT, (0, 0, 255))  # Blue title
    draw_text(draw, "Dr. Sample, MBBS, MD", 40, 80)
    draw_text(draw, "123 Medical Street, City, State, ZIP", 40, 100)
    draw_text(draw, "Phone: +91 1234567890 | Reg No: REG123456", 40, 120)
    draw_line(draw, (40, 150), (WIDTH - 40, 150), LINE_COLOR, 2)  # Blue line

    # Patient Info (grid-like)
    y = 170
    draw_text(draw, f"Name: {patient['name']}", 40, y)
    draw_text(draw, f"ID: {patient['id']}", 300, y)
    y += 30
    draw_text(draw, f"Age: {patient['age']}", 40, y)
    draw_text(draw, f"Gender: {patient['gender']}", 300, y)
    y += 30
    draw_text(draw, f"Contact: {patient['contact']}", 40, y)
    y += 30
    draw_text(draw, f"Date: {date}", 40, y)

    # Medications
    y += 50
    draw_text(draw, "MEDICATIONS", 40, y, BOLD_FONT)
    y += 30

    # Table header
    table_x = 40
    col_widths = [200, 150, 150]  # Medicine, Frequency, Duration
    draw_rectangle(draw, (table_x, y, table_x + sum(col_widths), y + 25), fill=BLUE_COLOR)
    draw_text(draw, "Medicine", table_x + 10, y + 5, BOLD_FONT, (255, 255, 255))
    draw_text(draw, "Frequency", table_x + col_widths[0] + 10, y + 5, BOLD_FONT, (255, 255, 255))
    draw_text(draw, "Duration", table_x + sum(col_widths[:2]) + 10, y + 5, BOLD_FONT, (255, 255, 255))
    y += 25

    # Table rows
    for med in medicines:
        draw_rectangle(draw, (table_x, y, table_x + sum(col_widths), y + 25), fill=(245, 245, 245))  # Whitesmoke
        draw_text(draw, med['name'], table_x + 10, y + 5)
        draw_text(draw, med['frequency'], table_x + col_widths[0] + 10, y + 5)
        draw_text(draw, med['duration'], table_x + sum(col_widths[:2]) + 10, y + 5)
        y += 25

    # Draw full table grid
    for i in range(len(medicines) + 2):  # +header + bottom
        draw_line(draw, (table_x, y - 25 * (len(medicines) + 1 - i)), (table_x + sum(col_widths), y - 25 * (len(medicines) + 1 - i)))
    for col in [0] + [sum(col_widths[:j+1]) for j in range(len(col_widths))]:
        draw_line(draw, (table_x + col, y - 25 * (len(medicines) + 1)), (table_x + col, y))

    # Signature
    y += 50
    draw_text(draw, "Signature: _________________________", 40, y)
    y += 30
    draw_text(draw, "Dr. Sample, MBBS, MD", 40, y, BOLD_FONT)

    # Save
    img.save(file_path)
    print(f"Generated → {file_path}")

# Generate 10 Prescriptions Automatically
for i in range(1, 51):
    generate_prescription(i)

print("\nAll prescription images generated successfully!")
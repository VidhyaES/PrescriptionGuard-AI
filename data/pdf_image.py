import fitz  # PyMuPDF
import os

def convert_pdfs_to_images(pdf_folder, output_folder, dpi=200):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all PDF files in the folder
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            doc = fitz.open(pdf_path)

            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Render page to image
                pix = page.get_pixmap(dpi=dpi)
                output_path = os.path.join(
                    output_folder,
                    f"{os.path.splitext(filename)[0]}.png"
                )
                pix.save(output_path)

            doc.close()
            print(f"Converted: {filename}")

# Example usage
pdf_folder = r"prescriptions"
output_folder =r"images\interaction"
convert_pdfs_to_images(pdf_folder, output_folder)
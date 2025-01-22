import os
from pathlib import Path

from annotation.extraction import extract_text_from_pdf
from scarper.consts import ANNOTATION_FILES_DIR, SAVE_DIR

if __name__ == '__main__':
    for item in os.listdir(SAVE_DIR):
        pdf_path = Path(f"{SAVE_DIR}/{item}").absolute()
        if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
            continue
        
        screenplay_text = extract_text_from_pdf(str(pdf_path))
        print(rf"{screenplay_text}")
        
        output_path = Path(ANNOTATION_FILES_DIR) / f"{pdf_path.stem}.txt"
        with output_path.open("w", encoding="utf-8") as f:
            f.write(screenplay_text)

import os
from pathlib import Path

from scarper.consts import SAVE_DIR


def download_pdf(pdf_url, filename):
    """Download the PDF file and save it."""
    import requests
    response = requests.get(pdf_url)
    if response.status_code == 200:
        file_path = os.path.join(str(Path(SAVE_DIR).absolute()), filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded PDF: {filename}")
    else:
        print(f"Failed to download PDF: {pdf_url}")
"""Módulo de OCR para extração de texto de imagens e PDFs.

Utiliza Tesseract OCR via pytesseract.
Requisitos do sistema:
  - tesseract-ocr instalado: sudo apt install tesseract-ocr tesseract-ocr-por
  - poppler-utils para PDF: sudo apt install poppler-utils
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_image(image_path: str) -> str | None:
    """Extrai texto de uma imagem usando Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang="por")
        text = text.strip()
        return text if text else None
    except Exception:
        return None


def extract_text_from_pdf(pdf_path: str) -> str | None:
    """Extrai texto de um PDF convertendo páginas em imagens e aplicando OCR."""
    try:
        pages = convert_from_path(pdf_path, dpi=300)
        full_text = []

        for page in pages:
            text = pytesseract.image_to_string(page, lang="por")
            if text.strip():
                full_text.append(text.strip())

        result = "\n\n".join(full_text)
        return result if result else None
    except Exception:
        return None

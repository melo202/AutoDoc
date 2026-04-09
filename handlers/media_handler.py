"""Handler para download e processamento de mídia recebida via WhatsApp."""

import os
import tempfile

import requests
from PIL import Image

import config
from ocr.processor import extract_text_from_image, extract_text_from_pdf


def download_media(media_url: str) -> str | None:
    """Faz download da mídia do Twilio e retorna o caminho do arquivo temporário."""
    try:
        response = requests.get(
            media_url,
            auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
            timeout=30,
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "pdf" in content_type:
            suffix = ".pdf"
        elif "image" in content_type:
            suffix = ".jpg"
        else:
            return None

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(response.content)
        tmp.close()
        return tmp.name

    except requests.RequestException:
        return None


def process_media(media_url: str, media_type: str) -> str | None:
    """Processa mídia recebida: faz download e extrai texto via OCR."""
    file_path = download_media(media_url)
    if not file_path:
        return None

    try:
        if "pdf" in media_type:
            text = extract_text_from_pdf(file_path)
        elif "image" in media_type:
            text = extract_text_from_image(file_path)
        else:
            text = None

        return text
    finally:
        if os.path.exists(file_path):
            os.unlink(file_path)

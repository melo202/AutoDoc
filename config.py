import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "autodoc-secret-key")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

NGROK_URL = os.getenv("NGROK_URL", "")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "documents", "templates")

DOCUMENT_TYPES = {
    "1": "procuracao_contrato",
    "2": "declaracao",
    "3": "contrato_locacao",
}

DOCUMENT_LABELS = {
    "procuracao_contrato": "Procuração + Contrato Advocatício",
    "declaracao": "Declaração",
    "contrato_locacao": "Contrato de Locação",
}

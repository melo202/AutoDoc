"""Gerador de documentos PDF.

- Procuração + Contrato Advocatício: usa reportlab (scripts/gerar_documentos.py)
- Declaração / Contrato de Locação: usa Jinja2 + WeasyPrint (templates HTML)
"""

import os
import uuid
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

import config
from scripts.gerar_documentos import gerar_procuracao, gerar_contrato, _file_name


def generate_pdf(document_type: str, data: dict) -> str | None:
    """Gera PDF(s) baseado no tipo de documento. Retorna caminho ou None."""
    if document_type == "procuracao_contrato":
        return _generate_procuracao_contrato(data)
    return _generate_from_template(document_type, data)


def _generate_procuracao_contrato(data: dict) -> str | None:
    """Gera Procuração + Contrato usando reportlab. Retorna caminho da pasta."""
    try:
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        nome = data["nome"]

        proc_path = os.path.join(config.OUTPUT_DIR, _file_name("Procuracao", nome))
        cont_path = os.path.join(config.OUTPUT_DIR, _file_name("Contrato", nome))

        gerar_procuracao(data, proc_path)
        gerar_contrato(data, cont_path)

        return f"{proc_path}\n{cont_path}"

    except Exception as e:
        print(f"Erro ao gerar Procuração/Contrato: {e}")
        return None


def _generate_from_template(document_type: str, data: dict) -> str | None:
    """Gera PDF a partir de template HTML (Declaração, Contrato de Locação)."""
    try:
        env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))
        template = env.get_template(f"{document_type}.html")

        data["data_atual"] = datetime.now().strftime("%d de %B de %Y")
        html_content = template.render(**data)

        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{document_type}_{timestamp}_{unique_id}.pdf"
        output_path = os.path.join(config.OUTPUT_DIR, filename)

        HTML(string=html_content).write_pdf(output_path)
        return output_path

    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

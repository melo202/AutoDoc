"""Gerador de documentos PDF a partir de templates HTML."""

import os
import uuid
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

import config


def generate_pdf(document_type: str, data: dict) -> str | None:
    """Gera um PDF a partir do template HTML e dos dados coletados.

    Args:
        document_type: Tipo do documento (ex: 'contrato_prestacao_servicos').
        data: Dicionário com os dados coletados do usuário.

    Returns:
        Caminho do arquivo PDF gerado ou None em caso de erro.
    """
    try:
        # Configurar Jinja2
        env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))
        template = env.get_template(f"{document_type}.html")

        # Adicionar data atual aos dados
        data["data_atual"] = datetime.now().strftime("%d de %B de %Y")

        # Renderizar HTML com os dados
        html_content = template.render(**data)

        # Garantir que o diretório de saída existe
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{document_type}_{timestamp}_{unique_id}.pdf"
        output_path = os.path.join(config.OUTPUT_DIR, filename)

        # Gerar PDF
        HTML(string=html_content).write_pdf(output_path)

        return output_path

    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

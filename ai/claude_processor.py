"""Processador de IA usando Claude Haiku para extração inteligente de dados via OCR.

Custo estimado: ~$0.001 por chamada (Haiku é o modelo mais barato).
Duas chamadas por cliente (CNH + comprovante) ≈ $0.002 por documento gerado.

Se ANTHROPIC_API_KEY não estiver configurada, o sistema funciona
normalmente sem IA (o usuário digita os dados manualmente).
"""

import json
import os

try:
    import anthropic
    _CLAUDE_AVAILABLE = True
except ImportError:
    _CLAUDE_AVAILABLE = False


HAIKU_MODEL = "claude-haiku-4-5-20251001"


def is_available() -> bool:
    """Verifica se a integração com Claude está disponível."""
    return _CLAUDE_AVAILABLE and bool(os.getenv("ANTHROPIC_API_KEY"))


def extract_from_cnh(ocr_text: str) -> dict:
    """Extrai nome e CPF do texto OCR de uma CNH."""
    if not is_available():
        return {}

    prompt = (
        "Extraia os dados de uma CNH brasileira do texto OCR abaixo.\n"
        "Retorne APENAS um JSON válido com os campos encontrados:\n"
        "- nome: nome completo em CAIXA ALTA\n"
        "- cpf: formatado como xxx.xxx.xxx-xx\n"
        "- nacionalidade: inferir 'brasileira' ou 'brasileiro'\n\n"
        "Se um campo não for encontrado, omita-o do JSON.\n\n"
        f"Texto OCR:\n{ocr_text}"
    )
    return _call_claude(prompt)


def extract_from_comprovante(ocr_text: str) -> dict:
    """Extrai endereço do texto OCR de um comprovante de endereço."""
    if not is_available():
        return {}

    prompt = (
        "Extraia o endereço completo deste comprovante de endereço.\n"
        "Retorne APENAS um JSON válido com o campo:\n"
        "- endereco: endereço completo no formato "
        '"Rua X, nº Y, Bairro, Cidade – UF, CEP XX.XXX-XXX"\n\n'
        "Se possível, extraia também:\n"
        "- cidade: no formato 'Cidade - UF'\n\n"
        f"Texto OCR:\n{ocr_text}"
    )
    return _call_claude(prompt)


def extract_from_document(ocr_text: str) -> dict:
    """Extrai dados genéricos de qualquer documento via OCR."""
    if not is_available():
        return {}

    prompt = (
        "Extraia todos os dados pessoais que encontrar neste documento.\n"
        "Retorne APENAS um JSON válido. Campos possíveis:\n"
        "- nome: CAIXA ALTA\n"
        "- cpf: formatado xxx.xxx.xxx-xx\n"
        "- endereco: endereço completo\n"
        "- nacionalidade\n"
        "- estado_civil\n"
        "- profissao\n\n"
        f"Texto OCR:\n{ocr_text}"
    )
    return _call_claude(prompt)


def detect_document_type(ocr_text: str) -> str:
    """Detecta se o documento é CNH, comprovante de endereço ou outro."""
    if not is_available():
        return "outro"

    prompt = (
        "Analise o texto OCR abaixo e classifique o documento.\n"
        "Retorne APENAS um JSON: {\"tipo\": \"cnh\"} ou "
        "{\"tipo\": \"comprovante\"} ou {\"tipo\": \"outro\"}\n\n"
        f"Texto OCR:\n{ocr_text[:500]}"
    )
    result = _call_claude(prompt)
    return result.get("tipo", "outro")


def _call_claude(prompt: str) -> dict:
    """Faz uma chamada ao Claude Haiku e retorna o JSON extraído."""
    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text.strip()

        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(response_text[start:end])

        return {}
    except Exception:
        return {}

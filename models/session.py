"""Gerenciamento de sessão do usuário no chatbot.

Cada usuário (número WhatsApp) tem uma sessão com:
- Estado atual do fluxo de conversa
- Tipo de documento selecionado
- Dados coletados até o momento
- Dados extraídos via OCR
"""

from datetime import datetime


# Armazena sessões em memória (dict indexado por número do WhatsApp)
_sessions: dict[str, dict] = {}


def get_session(sender: str) -> dict:
    """Retorna a sessão do usuário ou cria uma nova."""
    if sender not in _sessions:
        _sessions[sender] = _create_new_session()
    return _sessions[sender]


def reset_session(sender: str) -> dict:
    """Reseta a sessão do usuário."""
    _sessions[sender] = _create_new_session()
    return _sessions[sender]


def update_session(sender: str, **kwargs) -> dict:
    """Atualiza campos da sessão do usuário."""
    session = get_session(sender)
    session.update(kwargs)
    session["updated_at"] = datetime.now().isoformat()
    return session


def _create_new_session() -> dict:
    """Cria uma nova sessão vazia."""
    return {
        "state": "MENU",
        "document_type": None,
        "current_field_index": 0,
        "data": {},
        "ocr_text": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

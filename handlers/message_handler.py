"""Handler principal de mensagens do WhatsApp.

Roteia mensagens para o fluxo correto baseado no estado da sessão.
"""

import config
from models.session import get_session, reset_session, update_session
from handlers.media_handler import process_media
from flows.base_flow import get_flow_for_document


MENU_TEXT = (
    "Olá! Bem-vindo ao *AutoDoc* - Gerador de Documentos.\n\n"
    "Escolha o tipo de documento que deseja gerar:\n\n"
    "1️⃣ Contrato de Prestação de Serviços\n"
    "2️⃣ Procuração\n"
    "3️⃣ Declaração\n"
    "4️⃣ Contrato de Locação\n\n"
    "Digite o número da opção desejada.\n"
    "A qualquer momento, digite *menu* para voltar ao início."
)


def handle_incoming_message(
    sender: str,
    message: str,
    media_url: str | None,
    media_type: str | None,
) -> tuple[str, str | None]:
    """Processa mensagem recebida e retorna (texto_resposta, media_url_resposta)."""

    # Comando para voltar ao menu
    if message.lower() in ("menu", "inicio", "início", "voltar", "sair"):
        reset_session(sender)
        return MENU_TEXT, None

    session = get_session(sender)
    state = session["state"]

    # --- Estado: MENU (escolher tipo de documento) ---
    if state == "MENU":
        return _handle_menu(sender, message)

    # --- Estado: COLLECTING_DATA (coletando dados campo a campo) ---
    if state == "COLLECTING_DATA":
        return _handle_collecting(sender, message, media_url, media_type)

    # --- Estado: WAITING_OCR (esperando documento para OCR) ---
    if state == "WAITING_OCR":
        return _handle_ocr(sender, message, media_url, media_type)

    # --- Estado: CONFIRMING (confirmando dados) ---
    if state == "CONFIRMING":
        return _handle_confirming(sender, message)

    # Fallback
    reset_session(sender)
    return MENU_TEXT, None


def _handle_menu(sender: str, message: str) -> tuple[str, str | None]:
    """Processa seleção do tipo de documento."""
    doc_key = config.DOCUMENT_TYPES.get(message)

    if not doc_key:
        return (
            "Opção inválida. Por favor, digite um número de 1 a 4.\n\n" + MENU_TEXT,
            None,
        )

    doc_label = config.DOCUMENT_LABELS[doc_key]
    update_session(sender, document_type=doc_key, state="COLLECTING_DATA", current_field_index=0)

    flow = get_flow_for_document(doc_key)
    first_field = flow.get_current_field_prompt(0)

    return (
        f"Você selecionou: *{doc_label}*\n\n"
        f"Vou coletar as informações necessárias.\n"
        f"Você pode enviar uma *foto de documento* (RG, CPF, etc.) "
        f"a qualquer momento para extrair dados via OCR.\n\n"
        f"{first_field}"
    ), None


def _handle_collecting(
    sender: str,
    message: str,
    media_url: str | None,
    media_type: str | None,
) -> tuple[str, str | None]:
    """Coleta dados campo a campo."""
    session = get_session(sender)
    flow = get_flow_for_document(session["document_type"])

    # Se recebeu mídia, processar OCR
    if media_url:
        ocr_text = process_media(media_url, media_type)
        if ocr_text:
            update_session(sender, ocr_text=ocr_text)
            return (
                f"Texto extraído do documento:\n\n"
                f"_{ocr_text[:1000]}_\n\n"
                f"Os dados extraídos podem ser usados para preencher os campos.\n"
                f"Continue respondendo as perguntas abaixo.\n\n"
                f"{flow.get_current_field_prompt(session['current_field_index'])}"
            ), None
        else:
            return (
                "Não consegui ler o documento. Tente enviar uma imagem mais nítida.\n\n"
                f"{flow.get_current_field_prompt(session['current_field_index'])}"
            ), None

    # Salvar resposta no campo atual
    field_index = session["current_field_index"]
    field_name = flow.get_field_name(field_index)
    session["data"][field_name] = message
    next_index = field_index + 1

    # Verificar se todos os campos foram preenchidos
    if next_index >= flow.total_fields():
        update_session(sender, current_field_index=next_index, state="CONFIRMING")
        summary = flow.format_summary(session["data"])
        return (
            f"Todos os dados foram coletados!\n\n"
            f"*Resumo:*\n{summary}\n\n"
            f"Os dados estão corretos?\n"
            f"Digite *sim* para gerar o documento ou *não* para recomeçar."
        ), None

    update_session(sender, current_field_index=next_index)
    next_prompt = flow.get_current_field_prompt(next_index)
    return next_prompt, None


def _handle_ocr(
    sender: str,
    message: str,
    media_url: str | None,
    media_type: str | None,
) -> tuple[str, str | None]:
    """Processa documento enviado para OCR."""
    if not media_url:
        return "Por favor, envie uma imagem ou PDF do documento.", None

    ocr_text = process_media(media_url, media_type)
    if ocr_text:
        update_session(sender, ocr_text=ocr_text, state="COLLECTING_DATA")
        session = get_session(sender)
        flow = get_flow_for_document(session["document_type"])
        return (
            f"Texto extraído:\n\n_{ocr_text[:1000]}_\n\n"
            f"{flow.get_current_field_prompt(session['current_field_index'])}"
        ), None

    return "Não consegui extrair texto. Envie uma imagem mais nítida.", None


def _handle_confirming(sender: str, message: str) -> tuple[str, str | None]:
    """Confirma dados e gera documento."""
    if message.lower() in ("sim", "s", "yes", "ok"):
        session = get_session(sender)
        flow = get_flow_for_document(session["document_type"])

        from documents.generator import generate_pdf

        pdf_path = generate_pdf(session["document_type"], session["data"])

        if pdf_path:
            # Enviar o PDF de volta pelo Twilio requer hospedar o arquivo
            # Em produção, usar S3 ou similar. Aqui salvamos localmente.
            doc_label = config.DOCUMENT_LABELS[session["document_type"]]
            reset_session(sender)
            return (
                f"Documento *{doc_label}* gerado com sucesso!\n\n"
                f"O arquivo foi salvo em: {pdf_path}\n\n"
                f"Para hospedar e enviar o PDF via WhatsApp, configure um "
                f"serviço de armazenamento (S3, etc.) e exponha a URL pública.\n\n"
                f"Digite *menu* para gerar outro documento."
            ), None
        else:
            return "Erro ao gerar o documento. Tente novamente.", None

    elif message.lower() in ("não", "nao", "n", "no"):
        reset_session(sender)
        return "Vamos recomeçar.\n\n" + MENU_TEXT, None

    return "Por favor, digite *sim* ou *não*.", None

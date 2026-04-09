"""Handler principal de mensagens do WhatsApp.

Roteia mensagens para o fluxo correto baseado no estado da sessão.
Suporta dois modos:
- Fluxo sequencial (Declaração, Contrato de Locação)
- Fluxo inteligente com IA (Procuração + Contrato Advocatício)
"""

import config
from models.session import get_session, reset_session, update_session
from handlers.media_handler import process_media
from flows.base_flow import get_flow_for_document
from flows.procuracao_contrato import ProcuracaoContratoFlow
from ai import claude_processor


MENU_TEXT = (
    "Olá! Bem-vindo ao *AutoDoc* - Gerador de Documentos.\n\n"
    "Escolha o tipo de documento que deseja gerar:\n\n"
    "1️⃣ Procuração + Contrato Advocatício\n"
    "2️⃣ Declaração\n"
    "3️⃣ Contrato de Locação\n\n"
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

    if message.lower() in ("menu", "inicio", "início", "voltar", "sair"):
        reset_session(sender)
        return MENU_TEXT, None

    session = get_session(sender)
    state = session["state"]

    # --- MENU ---
    if state == "MENU":
        return _handle_menu(sender, message)

    # --- Fluxo inteligente: Procuração + Contrato ---
    if session.get("document_type") == "procuracao_contrato":
        if state == "UPLOAD_DOCS":
            return _handle_upload_docs(sender, message, media_url, media_type)
        if state == "COLLECTING_SMART":
            return _handle_smart_collecting(sender, message, media_url, media_type)
        if state == "CONFIRMING":
            return _handle_confirming_smart(sender, message)

    # --- Fluxo sequencial: Declaração / Contrato de Locação ---
    if state == "COLLECTING_DATA":
        return _handle_collecting(sender, message, media_url, media_type)
    if state == "CONFIRMING":
        return _handle_confirming(sender, message)

    reset_session(sender)
    return MENU_TEXT, None


# ============================================================
# MENU
# ============================================================


def _handle_menu(sender: str, message: str) -> tuple[str, str | None]:
    """Processa seleção do tipo de documento."""
    doc_key = config.DOCUMENT_TYPES.get(message)

    if not doc_key:
        return (
            "Opção inválida. Por favor, digite um número de 1 a 3.\n\n" + MENU_TEXT,
            None,
        )

    doc_label = config.DOCUMENT_LABELS[doc_key]

    # Fluxo inteligente para procuração + contrato
    if doc_key == "procuracao_contrato":
        update_session(sender, document_type=doc_key, state="UPLOAD_DOCS")
        flow = ProcuracaoContratoFlow()

        ai_status = ""
        if claude_processor.is_available():
            ai_status = "🤖 *IA ativa* - vou extrair dados automaticamente dos documentos.\n\n"
        else:
            ai_status = "ℹ️ IA indisponível - os dados serão preenchidos manualmente.\n\n"

        return (
            f"Você selecionou: *{doc_label}*\n\n"
            f"{ai_status}"
            f"{flow.get_upload_prompt()}"
        ), None

    # Fluxo sequencial para outros documentos
    update_session(
        sender, document_type=doc_key, state="COLLECTING_DATA", current_field_index=0
    )
    flow = get_flow_for_document(doc_key)
    first_field = flow.get_current_field_prompt(0)

    return (
        f"Você selecionou: *{doc_label}*\n\n"
        f"Vou coletar as informações necessárias.\n"
        f"Você pode enviar uma *foto de documento* a qualquer momento "
        f"para extrair dados via OCR.\n\n"
        f"{first_field}"
    ), None


# ============================================================
# FLUXO INTELIGENTE: Procuração + Contrato
# ============================================================


def _handle_upload_docs(
    sender: str,
    message: str,
    media_url: str | None,
    media_type: str | None,
) -> tuple[str, str | None]:
    """Fase de upload: recebe documentos para OCR + IA."""
    session = get_session(sender)
    flow = ProcuracaoContratoFlow()

    # Usuário quer pular para preenchimento manual
    if message.lower() in ("pular", "skip", "continuar", "pronto"):
        update_session(sender, state="COLLECTING_SMART")
        next_field = flow.get_next_missing_field(session["data"])
        if next_field:
            return next_field[2], None
        # Improvável mas possível: todos os campos já preenchidos
        update_session(sender, state="CONFIRMING")
        return _show_summary(flow, session["data"]), None

    # Recebeu mídia → processar OCR + IA
    if media_url:
        ocr_text = process_media(media_url, media_type)
        if not ocr_text:
            return (
                "Não consegui ler o documento. Tente uma imagem mais nítida.\n\n"
                "Envie outro documento ou digite *pular* para continuar.",
                None,
            )

        extracted = {}

        if claude_processor.is_available():
            # IA detecta o tipo e extrai campos
            doc_type = claude_processor.detect_document_type(ocr_text)
            if doc_type == "cnh":
                extracted = claude_processor.extract_from_cnh(ocr_text)
            elif doc_type == "comprovante":
                extracted = claude_processor.extract_from_comprovante(ocr_text)
            else:
                extracted = claude_processor.extract_from_document(ocr_text)
        else:
            # Sem IA: mostrar texto bruto
            return (
                f"Texto extraído do documento:\n\n_{ocr_text[:800]}_\n\n"
                f"Sem IA ativa, os dados precisam ser digitados manualmente.\n"
                f"Envie outro documento ou digite *pular* para continuar.",
                None,
            )

        if extracted:
            # Mesclar dados extraídos (não sobrescrever dados já preenchidos)
            for key, value in extracted.items():
                if key not in session["data"] or not session["data"][key]:
                    session["data"][key] = value

            update_session(sender)
            filled = flow.filled_count(session["data"])
            total = flow.total_fields()
            missing = flow.get_missing_fields(session["data"])

            extracted_str = "\n".join(
                f"  ✅ *{k}*: {v}" for k, v in extracted.items()
            )

            return (
                f"Dados extraídos com sucesso!\n\n{extracted_str}\n\n"
                f"Progresso: {filled}/{total} campos preenchidos.\n"
                f"Faltam: {len(missing)} campos.\n\n"
                f"Envie mais documentos ou digite *pular* para preencher o restante.",
                None,
            )

        return (
            f"Documento processado mas não consegui extrair dados estruturados.\n"
            f"Texto OCR: _{ocr_text[:500]}_\n\n"
            f"Envie outro documento ou digite *pular* para continuar.",
            None,
        )

    # Mensagem de texto durante upload (sem mídia)
    return (
        "Envie uma *foto* ou *PDF* de documento (CNH, comprovante, etc.)\n"
        "Ou digite *pular* para preencher manualmente.",
        None,
    )


def _handle_smart_collecting(
    sender: str,
    message: str,
    media_url: str | None,
    media_type: str | None,
) -> tuple[str, str | None]:
    """Coleta inteligente: pergunta apenas campos faltantes."""
    session = get_session(sender)
    flow = ProcuracaoContratoFlow()

    # Se recebeu mídia durante coleta, processar OCR
    if media_url:
        ocr_text = process_media(media_url, media_type)
        if ocr_text and claude_processor.is_available():
            extracted = claude_processor.extract_from_document(ocr_text)
            for key, value in extracted.items():
                if key not in session["data"] or not session["data"][key]:
                    session["data"][key] = value
            update_session(sender)

            if flow.is_complete(session["data"]):
                update_session(sender, state="CONFIRMING")
                return _show_summary(flow, session["data"]), None

            next_field = flow.get_next_missing_field(session["data"])
            extracted_str = ", ".join(f"{k}: {v}" for k, v in extracted.items())
            return (
                f"Dados extraídos: {extracted_str}\n\n{next_field[2]}",
                None,
            )

    # Salvar resposta no campo atual pendente
    next_field = flow.get_next_missing_field(session["data"])
    if next_field:
        field_name = next_field[0]
        session["data"][field_name] = message
        update_session(sender)

    # Verificar se está completo
    if flow.is_complete(session["data"]):
        update_session(sender, state="CONFIRMING")
        return _show_summary(flow, session["data"]), None

    # Próximo campo
    next_field = flow.get_next_missing_field(session["data"])
    if next_field:
        filled = flow.filled_count(session["data"])
        total = flow.total_fields()
        return f"({filled}/{total}) {next_field[2]}", None

    update_session(sender, state="CONFIRMING")
    return _show_summary(flow, session["data"]), None


def _handle_confirming_smart(sender: str, message: str) -> tuple[str, str | None]:
    """Confirmação para fluxo Procuração + Contrato."""
    if message.lower() in ("sim", "s", "yes", "ok"):
        session = get_session(sender)
        flow = ProcuracaoContratoFlow()
        final_data = flow.finalize_data(session["data"])

        from documents.generator import generate_pdf

        result = generate_pdf("procuracao_contrato", final_data)

        if result:
            nome = final_data["nome"]
            reset_session(sender)
            return (
                f"Documentos gerados com sucesso para *{nome}*!\n\n"
                f"Arquivos salvos:\n{result}\n\n"
                f"Digite *menu* para gerar outro documento."
            ), None
        else:
            return "Erro ao gerar os documentos. Tente novamente.", None

    elif message.lower() in ("não", "nao", "n", "no"):
        reset_session(sender)
        return "Vamos recomeçar.\n\n" + MENU_TEXT, None

    return "Por favor, digite *sim* ou *não*.", None


def _show_summary(flow: ProcuracaoContratoFlow, data: dict) -> str:
    """Formata mensagem de resumo com confirmação."""
    summary = flow.format_summary(data)
    return (
        f"Todos os dados foram coletados!\n\n"
        f"*Resumo:*\n{summary}\n\n"
        f"Os dados estão corretos?\n"
        f"Digite *sim* para gerar os documentos ou *não* para recomeçar."
    )


# ============================================================
# FLUXO SEQUENCIAL: Declaração / Contrato de Locação
# ============================================================


def _handle_collecting(
    sender: str,
    message: str,
    media_url: str | None,
    media_type: str | None,
) -> tuple[str, str | None]:
    """Coleta dados campo a campo (fluxo sequencial)."""
    session = get_session(sender)
    flow = get_flow_for_document(session["document_type"])

    if media_url:
        ocr_text = process_media(media_url, media_type)
        if ocr_text:
            update_session(sender, ocr_text=ocr_text)
            return (
                f"Texto extraído do documento:\n\n"
                f"_{ocr_text[:1000]}_\n\n"
                f"Continue respondendo as perguntas abaixo.\n\n"
                f"{flow.get_current_field_prompt(session['current_field_index'])}"
            ), None
        else:
            return (
                "Não consegui ler o documento. Tente uma imagem mais nítida.\n\n"
                f"{flow.get_current_field_prompt(session['current_field_index'])}"
            ), None

    field_index = session["current_field_index"]
    field_name = flow.get_field_name(field_index)
    session["data"][field_name] = message
    next_index = field_index + 1

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
    return flow.get_current_field_prompt(next_index), None


def _handle_confirming(sender: str, message: str) -> tuple[str, str | None]:
    """Confirmação para fluxo sequencial."""
    if message.lower() in ("sim", "s", "yes", "ok"):
        session = get_session(sender)

        from documents.generator import generate_pdf

        pdf_path = generate_pdf(session["document_type"], session["data"])

        if pdf_path:
            doc_label = config.DOCUMENT_LABELS[session["document_type"]]
            reset_session(sender)
            return (
                f"Documento *{doc_label}* gerado com sucesso!\n\n"
                f"Arquivo salvo em: {pdf_path}\n\n"
                f"Digite *menu* para gerar outro documento."
            ), None
        else:
            return "Erro ao gerar o documento. Tente novamente.", None

    elif message.lower() in ("não", "nao", "n", "no"):
        reset_session(sender)
        return "Vamos recomeçar.\n\n" + MENU_TEXT, None

    return "Por favor, digite *sim* ou *não*.", None

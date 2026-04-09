"""Fluxo de conversa para Procuração + Contrato Advocatício (skill combinada).

Este fluxo é inteligente:
- Aceita documentos (CNH, comprovante) e extrai dados via OCR + IA
- Pergunta apenas os campos que ainda faltam
- Gera dois PDFs ao final (Procuração + Contrato)
"""

from datetime import datetime


# Meses em português para data por extenso
_MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}

# Campos obrigatórios na ordem de coleta
FIELDS = [
    ("nome", "Nome Completo",
     "Informe o *nome completo do cliente* (CAIXA ALTA):"),
    ("cpf", "CPF",
     "Informe o *CPF* (formato: xxx.xxx.xxx-xx):"),
    ("nacionalidade", "Nacionalidade",
     "Informe a *nacionalidade* (ex: brasileira):"),
    ("estado_civil", "Estado Civil",
     "Informe o *estado civil*:"),
    ("profissao", "Profissão",
     "Informe a *profissão*:"),
    ("endereco", "Endereço Completo",
     "Informe o *endereço completo* (rua, nº, bairro, cidade – UF, CEP):"),
    ("acao", "Tipo de Ação",
     "Informe o *tipo de ação* (ex: Ação de Indenização por Danos Morais):"),
    ("vara", "Vara/Juízo",
     "Informe a *vara/juízo* (ex: Juízo Cível da Comarca de Goiânia – GO do TJGO).\n"
     "Ou digite *generica* para usar vara genérica:"),
    ("honorarios_valor", "Valor dos Honorários",
     "Informe o *valor dos honorários*.\nExemplos:\n"
     "- R$ 3.000,00 (três mil reais), a título de honorários de êxito\n"
     "- 20% sobre o valor da condenação\n"
     "Digite o valor completo:"),
    ("honorarios_pagamento", "Forma de Pagamento",
     "Informe a *forma de pagamento dos honorários*.\nExemplos:\n"
     "- Pagamento à vista na assinatura do contrato\n"
     "- 3 parcelas mensais de R$ 1.000,00\n"
     "Digite a forma de pagamento:"),
    ("cidade", "Cidade",
     "Informe a *cidade* para assinatura (ex: Goiânia - GO):"),
]

# Campos que podem ser extraídos via OCR
OCR_EXTRACTABLE = {"nome", "cpf", "nacionalidade", "endereco", "cidade"}


class ProcuracaoContratoFlow:
    """Fluxo combinado: Procuração Ad Judicia + Contrato Advocatício."""

    def get_next_missing_field(self, data: dict) -> tuple[str, str, str] | None:
        """Retorna o próximo campo que ainda não foi preenchido."""
        for name, label, prompt in FIELDS:
            if name not in data or not data[name]:
                return (name, label, prompt)
        return None

    def get_missing_fields(self, data: dict) -> list[tuple[str, str, str]]:
        """Retorna todos os campos que ainda faltam."""
        return [
            (name, label, prompt)
            for name, label, prompt in FIELDS
            if name not in data or not data[name]
        ]

    def total_fields(self) -> int:
        return len(FIELDS)

    def filled_count(self, data: dict) -> int:
        return sum(1 for name, _, _ in FIELDS if data.get(name))

    def is_complete(self, data: dict) -> bool:
        return self.get_next_missing_field(data) is None

    def format_summary(self, data: dict) -> str:
        """Formata resumo dos dados coletados."""
        lines = []
        for name, label, _ in FIELDS:
            value = data.get(name, "N/A")
            lines.append(f"- *{label}:* {value}")
        # Data é auto-gerada
        lines.append(f"- *Data:* {data.get('data', _data_extenso())}")
        return "\n".join(lines)

    def finalize_data(self, data: dict) -> dict:
        """Adiciona campos auto-gerados e normaliza os dados."""
        final = dict(data)

        # Auto-gerar data
        if "data" not in final or not final["data"]:
            final["data"] = _data_extenso()

        # Nome em CAIXA ALTA
        if "nome" in final:
            final["nome"] = final["nome"].upper()

        # Vara genérica se solicitado
        if final.get("vara", "").lower() in ("generica", "genérica", ""):
            cidade = final.get("cidade", "")
            uf = cidade.split("-")[-1].strip() if "-" in cidade else "GO"
            cidade_nome = cidade.split("-")[0].strip() if "-" in cidade else cidade
            final["vara"] = (
                f"Juízo Cível da Comarca de {cidade_nome} – {uf} do TJ{uf}"
            )

        return final

    def get_upload_prompt(self) -> str:
        """Mensagem para fase de upload de documentos."""
        return (
            "Você pode enviar *fotos de documentos* (CNH, comprovante de "
            "endereço, etc.) para extrair dados automaticamente via OCR.\n\n"
            "Envie os documentos agora, ou digite *pular* para preencher "
            "os dados manualmente."
        )


def _data_extenso() -> str:
    """Retorna data atual em formato extenso: '09 de abril de 2026'."""
    now = datetime.now()
    return f"{now.day:02d} de {_MESES[now.month]} de {now.year}"

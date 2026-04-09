"""Classe base para fluxos de conversa e factory para obter o fluxo correto."""

from flows.declaracao import DeclaracaoFlow
from flows.contrato_locacao import ContratoLocacaoFlow
from flows.procuracao_contrato import ProcuracaoContratoFlow


class BaseFlow:
    """Classe base para fluxos de coleta de dados sequencial."""

    FIELDS: list[tuple[str, str, str]] = []

    def get_current_field_prompt(self, index: int) -> str:
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][2]

    def get_field_name(self, index: int) -> str:
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][0]

    def get_field_label(self, index: int) -> str:
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][1]

    def total_fields(self) -> int:
        return len(self.FIELDS)

    def format_summary(self, data: dict) -> str:
        lines = []
        for field_name, label, _ in self.FIELDS:
            value = data.get(field_name, "N/A")
            lines.append(f"- *{label}:* {value}")
        return "\n".join(lines)


_FLOWS = {
    "declaracao": DeclaracaoFlow,
    "contrato_locacao": ContratoLocacaoFlow,
    "procuracao_contrato": ProcuracaoContratoFlow,
}


def get_flow_for_document(doc_type: str):
    """Retorna a instância do fluxo para o tipo de documento."""
    flow_class = _FLOWS.get(doc_type)
    if not flow_class:
        raise ValueError(f"Tipo de documento desconhecido: {doc_type}")
    return flow_class()

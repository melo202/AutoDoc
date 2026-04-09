"""Classe base para fluxos de conversa e factory para obter o fluxo correto."""

from flows.contrato_servicos import ContratoServicosFlow
from flows.procuracao import ProcuracaoFlow
from flows.declaracao import DeclaracaoFlow
from flows.contrato_locacao import ContratoLocacaoFlow


class BaseFlow:
    """Classe base para fluxos de coleta de dados."""

    # Lista de tuplas (nome_campo, rótulo, mensagem_prompt)
    FIELDS: list[tuple[str, str, str]] = []

    def get_current_field_prompt(self, index: int) -> str:
        """Retorna a mensagem de prompt para o campo atual."""
        if index >= len(self.FIELDS):
            return ""
        _, _, prompt = self.FIELDS[index]
        return prompt

    def get_field_name(self, index: int) -> str:
        """Retorna o nome interno do campo pelo índice."""
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][0]

    def get_field_label(self, index: int) -> str:
        """Retorna o rótulo do campo pelo índice."""
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][1]

    def total_fields(self) -> int:
        """Retorna o total de campos a serem coletados."""
        return len(self.FIELDS)

    def format_summary(self, data: dict) -> str:
        """Formata um resumo dos dados coletados."""
        lines = []
        for field_name, label, _ in self.FIELDS:
            value = data.get(field_name, "N/A")
            lines.append(f"- *{label}:* {value}")
        return "\n".join(lines)


_FLOWS = {
    "contrato_prestacao_servicos": ContratoServicosFlow,
    "procuracao": ProcuracaoFlow,
    "declaracao": DeclaracaoFlow,
    "contrato_locacao": ContratoLocacaoFlow,
}


def get_flow_for_document(doc_type: str) -> BaseFlow:
    """Retorna a instância do fluxo para o tipo de documento."""
    flow_class = _FLOWS.get(doc_type)
    if not flow_class:
        raise ValueError(f"Tipo de documento desconhecido: {doc_type}")
    return flow_class()

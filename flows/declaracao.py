"""Fluxo de conversa para Declaração."""


class DeclaracaoFlow:
    """Coleta de dados para Declaração."""

    FIELDS = [
        # --- Dados do Declarante ---
        ("declarante_nome", "Nome do Declarante",
         "Informe o *nome completo do declarante*:"),
        ("declarante_cpf", "CPF do Declarante",
         "Informe o *CPF do declarante*:"),
        ("declarante_rg", "RG do Declarante",
         "Informe o *RG do declarante*:"),
        ("declarante_nacionalidade", "Nacionalidade",
         "Informe a *nacionalidade do declarante*:"),
        ("declarante_estado_civil", "Estado Civil",
         "Informe o *estado civil do declarante*:"),
        ("declarante_profissao", "Profissão",
         "Informe a *profissão do declarante*:"),
        ("declarante_endereco", "Endereço do Declarante",
         "Informe o *endereço completo do declarante*:"),
        # --- Dados da Declaração ---
        ("tipo_declaracao", "Tipo de Declaração",
         "Qual o *tipo de declaração*? (residência, vínculo, renda, outro):"),
        ("conteudo", "Conteúdo da Declaração",
         "Descreva o *conteúdo/teor da declaração* (o que está sendo declarado):"),
        ("finalidade", "Finalidade",
         "Informe a *finalidade da declaração* (para que será utilizada):"),
        ("cidade_assinatura", "Cidade da Assinatura",
         "Informe a *cidade onde a declaração será assinada*:"),
    ]

    def get_current_field_prompt(self, index):
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][2]

    def get_field_name(self, index):
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][0]

    def get_field_label(self, index):
        if index >= len(self.FIELDS):
            return ""
        return self.FIELDS[index][1]

    def total_fields(self):
        return len(self.FIELDS)

    def format_summary(self, data):
        lines = []
        for field_name, label, _ in self.FIELDS:
            value = data.get(field_name, "N/A")
            lines.append(f"- *{label}:* {value}")
        return "\n".join(lines)

"""Fluxo de conversa para Procuração."""


class ProcuracaoFlow:
    """Coleta de dados para Procuração."""

    FIELDS = [
        # --- Dados do Outorgante (quem concede poderes) ---
        ("outorgante_nome", "Nome do Outorgante",
         "Informe o *nome completo do outorgante* (quem concede os poderes):"),
        ("outorgante_cpf", "CPF do Outorgante",
         "Informe o *CPF do outorgante*:"),
        ("outorgante_rg", "RG do Outorgante",
         "Informe o *RG do outorgante*:"),
        ("outorgante_nacionalidade", "Nacionalidade do Outorgante",
         "Informe a *nacionalidade do outorgante*:"),
        ("outorgante_estado_civil", "Estado Civil do Outorgante",
         "Informe o *estado civil do outorgante*:"),
        ("outorgante_profissao", "Profissão do Outorgante",
         "Informe a *profissão do outorgante*:"),
        ("outorgante_endereco", "Endereço do Outorgante",
         "Informe o *endereço completo do outorgante*:"),
        # --- Dados do Outorgado (quem recebe poderes) ---
        ("outorgado_nome", "Nome do Outorgado",
         "Informe o *nome completo do outorgado* (quem recebe os poderes):"),
        ("outorgado_cpf", "CPF do Outorgado",
         "Informe o *CPF do outorgado*:"),
        ("outorgado_rg", "RG do Outorgado",
         "Informe o *RG do outorgado*:"),
        ("outorgado_endereco", "Endereço do Outorgado",
         "Informe o *endereço completo do outorgado*:"),
        # --- Dados da Procuração ---
        ("poderes", "Poderes Concedidos",
         "Descreva os *poderes concedidos* ao outorgado:"),
        ("finalidade", "Finalidade da Procuração",
         "Informe a *finalidade específica* da procuração:"),
        ("cidade_assinatura", "Cidade da Assinatura",
         "Informe a *cidade onde a procuração será assinada*:"),
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

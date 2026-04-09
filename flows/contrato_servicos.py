"""Fluxo de conversa para Contrato de Prestação de Serviços."""


class ContratoServicosFlow:
    """Coleta de dados para Contrato de Prestação de Serviços."""

    FIELDS = [
        # --- Dados do Contratante ---
        ("contratante_nome", "Nome do Contratante",
         "Informe o *nome completo do contratante* (quem contrata o serviço):"),
        ("contratante_cpf", "CPF do Contratante",
         "Informe o *CPF do contratante*:"),
        ("contratante_rg", "RG do Contratante",
         "Informe o *RG do contratante*:"),
        ("contratante_endereco", "Endereço do Contratante",
         "Informe o *endereço completo do contratante* (rua, nº, bairro, cidade, estado, CEP):"),
        # --- Dados do Prestador ---
        ("prestador_nome", "Nome do Prestador",
         "Informe o *nome completo do prestador de serviços*:"),
        ("prestador_cpf", "CPF/CNPJ do Prestador",
         "Informe o *CPF ou CNPJ do prestador*:"),
        ("prestador_rg", "RG do Prestador",
         "Informe o *RG do prestador* (ou N/A se pessoa jurídica):"),
        ("prestador_endereco", "Endereço do Prestador",
         "Informe o *endereço completo do prestador*:"),
        # --- Dados do Contrato ---
        ("objeto", "Objeto do Contrato",
         "Descreva o *objeto do contrato* (qual serviço será prestado):"),
        ("valor", "Valor do Contrato",
         "Informe o *valor total do contrato* (ex: R$ 5.000,00):"),
        ("forma_pagamento", "Forma de Pagamento",
         "Informe a *forma de pagamento* (à vista, parcelado, mensal, etc.):"),
        ("prazo", "Prazo do Contrato",
         "Informe o *prazo de duração do contrato* (ex: 12 meses):"),
        ("cidade_assinatura", "Cidade da Assinatura",
         "Informe a *cidade onde o contrato será assinado*:"),
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

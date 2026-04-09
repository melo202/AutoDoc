"""Fluxo de conversa para Contrato de Locação."""


class ContratoLocacaoFlow:
    """Coleta de dados para Contrato de Locação de Imóvel."""

    FIELDS = [
        # --- Dados do Locador ---
        ("locador_nome", "Nome do Locador",
         "Informe o *nome completo do locador* (proprietário do imóvel):"),
        ("locador_cpf", "CPF do Locador",
         "Informe o *CPF do locador*:"),
        ("locador_rg", "RG do Locador",
         "Informe o *RG do locador*:"),
        ("locador_endereco", "Endereço do Locador",
         "Informe o *endereço completo do locador*:"),
        # --- Dados do Locatário ---
        ("locatario_nome", "Nome do Locatário",
         "Informe o *nome completo do locatário* (quem vai alugar):"),
        ("locatario_cpf", "CPF do Locatário",
         "Informe o *CPF do locatário*:"),
        ("locatario_rg", "RG do Locatário",
         "Informe o *RG do locatário*:"),
        ("locatario_endereco", "Endereço do Locatário",
         "Informe o *endereço atual do locatário*:"),
        # --- Dados do Imóvel ---
        ("imovel_endereco", "Endereço do Imóvel",
         "Informe o *endereço completo do imóvel* a ser locado:"),
        ("imovel_descricao", "Descrição do Imóvel",
         "Descreva o *imóvel* (tipo, quartos, área, etc.):"),
        # --- Dados do Contrato ---
        ("valor_aluguel", "Valor do Aluguel",
         "Informe o *valor mensal do aluguel* (ex: R$ 1.500,00):"),
        ("dia_vencimento", "Dia de Vencimento",
         "Informe o *dia de vencimento* do aluguel (ex: 10):"),
        ("prazo", "Prazo da Locação",
         "Informe o *prazo da locação* (ex: 30 meses):"),
        ("valor_caucao", "Valor da Caução",
         "Informe o *valor da caução/depósito* (ou N/A se não houver):"),
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

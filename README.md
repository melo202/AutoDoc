# AutoDoc - Chatbot WhatsApp para Geração de Documentos Jurídicos

Chatbot WhatsApp que coleta informações do solicitante via conversa, documentos (OCR) e IA (Claude) para gerar documentos jurídicos formatados em PDF.

## Documentos Suportados

- **Procuração + Contrato Advocatício** — Gera ambos os PDFs com reportlab (fluxo inteligente com IA)
- **Declaração** — Declarações diversas (residência, vínculo, renda, etc.)
- **Contrato de Locação** — Contrato de aluguel de imóvel

## Arquitetura

```
AutoDoc/
├── app.py                          # Servidor Flask + webhook Twilio
├── config.py                       # Configurações e variáveis de ambiente
├── requirements.txt                # Dependências Python
├── .env.example                    # Template de variáveis de ambiente
├── scripts/
│   └── gerar_documentos.py         # Gerador PDF com reportlab (skill procuração+contrato)
├── ai/
│   └── claude_processor.py         # Claude Haiku para extração inteligente de OCR
├── handlers/
│   ├── message_handler.py          # Roteamento de mensagens e fluxos
│   └── media_handler.py            # Download e processamento de mídia (OCR)
├── models/
│   └── session.py                  # Gerenciamento de sessão por usuário
├── ocr/
│   └── processor.py                # Extração de texto via Tesseract OCR
├── flows/
│   ├── base_flow.py                # Factory de fluxos de conversa
│   ├── procuracao_contrato.py      # Fluxo inteligente: Procuração + Contrato
│   ├── declaracao.py               # Fluxo: Declaração
│   └── contrato_locacao.py         # Fluxo: Contrato de Locação
├── documents/
│   ├── generator.py                # Dispatcher de geração de PDF
│   └── templates/                  # Templates HTML (declaração, locação)
└── output/                         # PDFs gerados
```

## Custo

| Componente | Custo |
|---|---|
| Tesseract OCR | Gratuito (local) |
| Flask + reportlab | Gratuito |
| Twilio WhatsApp Sandbox | Gratuito (teste) |
| Claude Haiku (IA) | ~$0.002 por documento (opcional) |
| ngrok | Gratuito (plano free) |

**Total estimado: $0.00 ~ $0.01 por documento.**

## Pré-requisitos

### Sistema

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-por poppler-utils

# macOS
brew install tesseract poppler
```

### Python 3.11+

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração

```bash
cp .env.example .env
```

Preencha no `.env`:

```
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token
ANTHROPIC_API_KEY=sua_chave    # opcional: para IA na extração de OCR
```

## Como Executar

```bash
# Terminal 1: servidor
python app.py

# Terminal 2: túnel público
ngrok http 5000
```

Configure o webhook no [Twilio Console](https://console.twilio.com/):
- URL: `https://SEU-NGROK-URL/webhook`
- Método: POST

## Fluxos de Uso

### Procuração + Contrato (com IA)

1. Usuário escolhe opção 1
2. Bot pede fotos de documentos (CNH, comprovante de endereço)
3. OCR + Claude Haiku extraem dados automaticamente (nome, CPF, endereço)
4. Bot pergunta apenas os campos que faltam (ação, honorários, etc.)
5. Bot exibe resumo e pede confirmação
6. Bot gera **dois PDFs**: Procuração Ad Judicia + Contrato Advocatício

### Declaração / Contrato de Locação

1. Usuário escolhe opção 2 ou 3
2. Bot coleta dados campo a campo
3. Usuário pode enviar foto para OCR a qualquer momento
4. Bot gera o PDF

## Geração standalone (sem chatbot)

```bash
python3 scripts/gerar_documentos.py '{"nome":"NOME COMPLETO",...}' ./output/
```

Consulte o manual da skill para o JSON completo de campos.

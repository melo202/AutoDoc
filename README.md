# AutoDoc - Chatbot WhatsApp para Geração de Documentos

Chatbot WhatsApp que coleta informações do solicitante via conversa e documentos (OCR) para gerar documentos jurídicos formatados em PDF.

## Documentos Suportados

- Contrato de Prestação de Serviços
- Procuração
- Declaração
- Contrato de Locação

## Arquitetura

```
AutoDoc/
├── app.py                          # Servidor Flask + webhook Twilio
├── config.py                       # Configurações e variáveis de ambiente
├── requirements.txt                # Dependências Python
├── .env.example                    # Template de variáveis de ambiente
├── handlers/
│   ├── message_handler.py          # Roteamento de mensagens e fluxo principal
│   └── media_handler.py            # Download e processamento de mídia (OCR)
├── models/
│   └── session.py                  # Gerenciamento de sessão por usuário
├── ocr/
│   └── processor.py                # Extração de texto via Tesseract OCR
├── flows/
│   ├── base_flow.py                # Factory de fluxos de conversa
│   ├── contrato_servicos.py        # Fluxo: Contrato de Prestação de Serviços
│   ├── procuracao.py               # Fluxo: Procuração
│   ├── declaracao.py               # Fluxo: Declaração
│   └── contrato_locacao.py         # Fluxo: Contrato de Locação
├── documents/
│   ├── generator.py                # Gerador de PDF (Jinja2 + WeasyPrint)
│   └── templates/                  # Templates HTML dos documentos
│       ├── contrato_prestacao_servicos.html
│       ├── procuracao.html
│       ├── declaracao.html
│       └── contrato_locacao.html
└── output/                         # PDFs gerados
```

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
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Configuração

1. Copie `.env.example` para `.env` e preencha suas credenciais:

```bash
cp .env.example .env
```

2. Configure suas credenciais do Twilio no `.env`:

```
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Como Executar

### 1. Iniciar o servidor Flask

```bash
python app.py
```

### 2. Iniciar o ngrok

```bash
ngrok http 5000
```

### 3. Configurar o webhook no Twilio

- Acesse o [Console do Twilio](https://console.twilio.com/)
- Vá em Messaging > Try it out > Send a WhatsApp message
- Configure o webhook URL: `https://SEU-NGROK-URL/webhook`
- Método: POST

### 4. Testar

Envie uma mensagem para o número do WhatsApp Sandbox do Twilio e siga o fluxo do chatbot.

## Fluxo de Uso

1. Usuário envia mensagem ao bot
2. Bot exibe menu com tipos de documentos
3. Usuário escolhe o documento (1-4)
4. Bot coleta dados campo a campo
5. Usuário pode enviar foto de documento para OCR
6. Bot exibe resumo e pede confirmação
7. Bot gera o PDF e informa o caminho do arquivo

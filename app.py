from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import config
from handlers.message_handler import handle_incoming_message

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY


@app.route("/webhook", methods=["POST"])
def webhook():
    """Endpoint que recebe mensagens do Twilio WhatsApp."""
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")
    num_media = int(request.form.get("NumMedia", 0))

    media_url = None
    media_type = None
    if num_media > 0:
        media_url = request.form.get("MediaUrl0", "")
        media_type = request.form.get("MediaContentType0", "")

    response_text, media_response = handle_incoming_message(
        sender=sender,
        message=incoming_msg,
        media_url=media_url,
        media_type=media_type,
    )

    resp = MessagingResponse()
    msg = resp.message(response_text)

    if media_response:
        msg.media(media_response)

    return str(resp)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "AutoDoc WhatsApp Bot"}


if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=5000)

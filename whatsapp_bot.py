"""
WhatsApp Bot интеграция
Использует Twilio API для WhatsApp Business
"""
import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import asyncio
from ai_assistant import ai_assistant

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)


def send_whatsapp_message(to_number: str, message: str, media_url: str = None):
    """Отправить сообщение в WhatsApp"""
    try:
        message_params = {
            'from_': TWILIO_WHATSAPP_NUMBER,
            'body': message,
            'to': f'whatsapp:{to_number}'
        }
        
        if media_url:
            message_params['media_url'] = [media_url]
        
        message = twilio_client.messages.create(**message_params)
        return message.sid
    except Exception as e:
        print(f"Ошибка отправки WhatsApp сообщения: {e}")
        return None


@app.route('/whatsapp/webhook', methods=['POST'])
async def whatsapp_webhook():
    """Webhook для получения сообщений от WhatsApp"""
    try:
        # Получаем данные от Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '').replace('whatsapp:', '')
        
        print(f"Получено сообщение от {sender}: {incoming_msg}")
        
        # Используем номер телефона как client_id
        client_id = sender.replace('+', '').replace('-', '')
        
        # Обрабатываем через AI-ассистента
        response_text = await ai_assistant.process_message(
            client_id=client_id,
            message=incoming_msg,
            channel="whatsapp"
        )
        
        # Отправляем ответ
        resp = MessagingResponse()
        resp.message(response_text)
        
        return str(resp)
        
    except Exception as e:
        print(f"Ошибка обработки WhatsApp webhook: {e}")
        resp = MessagingResponse()
        resp.message("Извините, произошла ошибка. Попробуйте ещё раз.")
        return str(resp)


@app.route('/whatsapp/send', methods=['POST'])
def whatsapp_send():
    """API для отправки сообщений в WhatsApp (для n8n)"""
    try:
        data = request.json
        to_number = data.get('to')
        message = data.get('message')
        media_url = data.get('media_url')
        
        message_sid = send_whatsapp_message(to_number, message, media_url)
        
        return {
            'status': 'sent',
            'message_sid': message_sid,
            'to': to_number
        }
        
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/whatsapp/broadcast', methods=['POST'])
def whatsapp_broadcast():
    """Массовая рассылка в WhatsApp (для контент-маркетинга)"""
    try:
        data = request.json
        recipients = data.get('recipients', [])  # Список номеров
        message = data.get('message')
        media_url = data.get('media_url')
        
        sent_count = 0
        failed = []
        
        for recipient in recipients:
            message_sid = send_whatsapp_message(recipient, message, media_url)
            if message_sid:
                sent_count += 1
            else:
                failed.append(recipient)
        
        return {
            'status': 'completed',
            'sent': sent_count,
            'failed': len(failed),
            'failed_numbers': failed
        }
        
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    print("WhatsApp Bot запущен")
    print(f"Webhook URL: /whatsapp/webhook")
    app.run(host='0.0.0.0', port=5001)

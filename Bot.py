from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Токен доступа и верификация
ACCESS_TOKEN = "IGQWRPZAmR4U2JlUkVRdmZA3UHhSMWRhMUJ4TTY2OWhSeElfUkExbHJpbU8zT0p0RHgxRGYydWVuZAVNxR3J3NTF3MFJGZAy1yVjlmZAF9laVZAYLUJZAVlo0XzBJdWFyNzF1eFh6TXJHc281UTJEYTBaQzR6TUhTRGJBTGsZD"
VERIFY_TOKEN = "trahal_anal_mamonta"

# Функция для отправки сообщений
def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения: {response.json()}")

# Обработка вебхуков
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')
        if token_sent == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Верификация не удалась', 403

    elif request.method == 'POST':
        output = request.get_json()
        for event in output.get('entry', []):
            for message in event.get('messaging', []):
                if 'message' in message:
                    sender_id = message['sender']['id']
                    message_text = message['message'].get('text')

                    # Простая логика ответа
                    if message_text:
                        if "привет" in message_text.lower():
                            send_message(sender_id, "Привет! Чем могу помочь?")
                        elif "товар" in message_text.lower():
                            send_message(sender_id, "Какой именно товар вас интересует? Мы предлагаем: 1) Категория А, 2) Категория Б.")
                        else:
                            send_message(sender_id, "Извините, я пока не понял вас. Могу помочь с выбором товаров!")
        return "Сообщение обработано", 200

if __name__ == '__main__':
    from waitress import serve  # Waitress лучше для Windows
    serve(app, host='0.0.0.0', port=5000)

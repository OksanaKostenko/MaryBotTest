import requests
import bot
import misc
from flask import Flask, request
import os

token = misc.token
url = "https://api.telegram.org/bot"

app = Flask(__name__)

def get_last_mess(data):
    last_object = data
    text = last_object['message']['text']
    chat_id = last_object['message']['chat']['id']
    message = {"chat_id": chat_id, "text": text}
    return message

def send_mess(chat_id, text):
    URL = url + token +"/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(URL, data=params)
    return response

@app.route("/" + token, methods=["POST"])
def process_update():
    if request.method == "POST":
        data = request.get_json()
        if "message" in data:
            chat_id = get_last_mess(data)["chat_id"]
            text = get_last_mess(data)["text"]
            bot_text = bot.chat(text)
            send_mess(chat_id, bot_text)
        return "ok!", 200
    return "..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

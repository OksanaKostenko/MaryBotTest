import requests
import bot
import misc
from flask import Flask, request
import os
from pymessenger.bot import Bot

token = misc.tlg_token
url = "https://api.telegram.org/bot"

ACCESS_TOKEN = misc.fb_access_token
VERIFY_TOKEN = misc.fb_verify_token
fb_bot = Bot(ACCESS_TOKEN)

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

@app.route("/", methods=['POST'])
def receive_message():
    if request.method == 'POST':
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    text = message['message'].get('text')
                    response_sent_text = bot.chat(text)
                    send_message_fb(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = "I'm sorry, I can't handle non text messages"
                    send_message_fb(recipient_id, response_sent_nontext)
    return "Message Processed"

#uses PyMessenger to send response to user
def send_message_fb(recipient_id, response):
    #sends user the text message provided via input response parameter
    fb_bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

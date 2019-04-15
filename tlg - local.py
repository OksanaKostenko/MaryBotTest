import requests
import bot
from time import sleep

token = "788723207:AAFv-9HVizlkJZlXzEWWPIPNSLy8njZC4RY"
url = "https://api.telegram.org/bot"

global last_update_id 
last_update_id = 0

def get_updates():
    URL = url + token +"/getUpdates"
    response = requests.get(URL)
    return response.json()

def get_last_mess(data):
    last_object = data['result'][-1]
    text = last_object['message']['text']
    chat_id = last_object['message']['chat']['id']
    update_id = last_object['update_id']
    message = {"chat_id": chat_id, "text": text, "update_id": update_id}
    return message

def send_mess(chat_id, text):
    URL = url + token +"/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(URL, data=params)
    return response

def main():
    pass
    while True:
        data = get_updates()
        chat_id = get_last_mess(data)["chat_id"]
        text = get_last_mess(data)["text"]
        update_id = get_last_mess(data)["update_id"]
        
        global last_update_id
        if last_update_id != update_id:
            bot_text = bot.chat(text)
            send_mess(chat_id, bot_text)
            last_update_id = update_id
        else:
            continue
        sleep(1)

if __name__ == "__main__":
    main()

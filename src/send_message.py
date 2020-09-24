import requests

import datetime


def log(message):
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")


last_update_id = 0

while True:
    offset = last_update_id + 1
    log(f"Sending request. offset = {offset}")
    url = "https://api.telegram.org/bot1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs/getUpdates"
    response = requests.get(url, params={
        "offset": offset,
        "timeout": 5
    })
    data = response.json()
    result = data["result"]
    for update in result:
        chat_id = update["message"]["chat"]["id"]
        message_text = update["message"]["text"]
        last_update_id = update["update_id"]
        log(f"Got new message. Chat id = {chat_id}, Message = {message_text}")

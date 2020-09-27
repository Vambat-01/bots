import requests

import datetime


def log(message):
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")

def make_get_request(url, params):
    log(f"Making a request: {url}")
    response = requests.get(url, params=params)
    log(f"Send message status code: {response.status_code}")
    return response

def search(text):
    response = make_get_request(f"https://api.stackexchange.com//2.2/search/advanced",{
        "order": "desc",
        "sort": "relevance",
        "title": text,
        "page": 1,
        "pagesize": 5,
        "site": "stackoverflow"
    })
    data = response.json()
    quota_remaining = data["quota_remaining"]
    log(f"Quota remaining: {quota_remaining}")
    accept_answer_id = data["items"][0]["accepted_answer_id"]
    return f"https://stackoverflow.com/a/{accept_answer_id}"



class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0

    def receive_update(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        offset = self.last_update_id + 1
        log(f"Sending request. offset = {offset}")
        response= requests.get(url, params={
            "offset": offset,
            "timeout": 5
        })
        data = response.json()
        result = data["result"]
        for update in result:
            chat_id = update["message"]["chat"]["id"]
            text_message = update["message"]["text"]
            self.last_update_id = update["update_id"]
            accepted_answer = search(text_message)
            self.send_message(chat_id, f"Your search: {text_message}. Search result: {accepted_answer}")

    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.get(url, params={
            "chat_id": chat_id,
            "text": text
        })



token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
bot = Bot(token)

while True:
    bot.receive_update()



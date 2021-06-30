import requests
import datetime
import os


class SearchError(Exception):
    def __init__(self, message):
        self.message = message


def log(message):
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")


def make_get_request(url, params):
    log(f"Making a request: {url}")
    response = requests.get(url, params=params)
    log(f"Send message status code: {response.status_code}")
    return response


def search_stackoverflow(text):
    response = make_get_request(f"https://api.stackexchange.com//2.2/search/advanced", {
        "order": "desc",
        "sort": "relevance",
        "title": text,
        "page": 1,
        "pagesize": 5
    })

    if response.status_code == 400:
        raise SearchError("The site is not responding. Try later.")
    data = response.json()
    quota_remaining = data["quota_remaining"]
    log(f"Quota remaining: {quota_remaining}")
    if len(data["items"]) == 0:
        raise SearchError("Answer not found")

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
        response = requests.get(url, params={
            "offset": offset,
            "timeout": 5
        })
        data = response.json()
        result = data["result"]
        for update in result:
            chat_id = update["message"]["chat"]["id"]
            text_message = update["message"]["text"]
            self.last_update_id = update["update_id"]
            try:
                accepted_answer = search_stackoverflow(text_message)
                self.send_message(chat_id, f"Your search: {text_message}. Search result: {accepted_answer}")
            except SearchError as error:
                self.send_message(chat_id, f"Your search: {text_message}. Got error:{error.message}")
                self.send_message(chat_id, f"Your search: {text_message}. Got error:{error.message}")

    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.get(url, params={
            "chat_id": chat_id,
            "text": text
        })


token = os.environ["BOT_TOKEN"]
bot = Bot(token)

while True:
    bot.receive_update()

import  requests

url = "https://api.telegram.org/bot1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs/getUpdates"
response = requests.get(url)
data = response.json()
result = data["result"]
for update in result:
    chat_id = update["message"]["chat"]["id"]
    print(chat_id)
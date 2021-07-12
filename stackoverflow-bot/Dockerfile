FROM python:3.7

COPY ./bot.py /app/bot.py
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./bot.py"]

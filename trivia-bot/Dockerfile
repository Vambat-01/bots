FROM python:3.7

RUN pip install fastapi uvicorn argparse asyncio dataclasses_json aiohttp redis 

COPY ./resources /app/resources
COPY ./core /app/core
COPY ./test /app/test
COPY ./trivia /app/trivia
COPY ./core /app/core
COPY ./main.py /app/main.py

WORKDIR /app

CMD ["python", "./main.py", "-config", "resources/config_server.json"]

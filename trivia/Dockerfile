FROM python:3.7

RUN pip install fastapi uvicorn argparse asyncio dataclasses_json aiohttp redis 

COPY ./resources /app/trivia/resources
COPY ./core /app/trivia/core
COPY ./test /app/trivia/test
COPY ./trivia /app/trivia/trivia
COPY ./core /app/trivia/core
COPY ./main.py /app/trivia/main.py

WORKDIR /app/trivia

CMD ["python", "./main.py", "-config", "resources/config_server.json"]
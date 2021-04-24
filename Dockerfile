FROM python:3.7

RUN pip install fastapi uvicorn argparse asyncio dataclasses_json aiohttp

EXPOSE 8000

COPY ./trivia/resources /app/trivia/resources
COPY ./trivia/core /app/trivia/core
COPY ./trivia/test /app/trivia/test
COPY ./trivia/trivia /app/trivia/trivia
COPY ./trivia/core /app/trivia/core
COPY ./trivia/main.py /app/trivia/main.py

WORKDIR /app/trivia

CMD ["python", "./main.py", "-file", "resources/bot_questions_mini.json", "-host", "127.0.0.1", "-port", "8000"]

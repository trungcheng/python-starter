FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY telegram-test-bot.py /src/bot.py

CMD ["python", "/src/bot.py"]
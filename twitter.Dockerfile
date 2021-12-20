FROM python:3.8-slim

RUN useradd --create-home --shell /bin/bash twitter_user
USER twitter_user

WORKDIR /home/twitter_user

COPY start_twitter_bot.py .

RUN mkdir -p bots/twitter

COPY requirements_twitter.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY bots/twitter /home/twitter_user/bots/twitter
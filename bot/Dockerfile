FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot
ADD bot_api_token.py config.py converter.py exceptions.py exchange_rates_parser.py user_query_parser.py requirements.txt main.py ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

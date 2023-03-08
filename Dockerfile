FROM python:3.10
ADD bot_api_token.py config.py converter.py exceptions.py exchange_rates_parser.py user_query_parser.py Pipfile Pipfile.lock main.py ./
RUN pip install pipenv
RUN pipenv install
RUN apt update && apt install -y \
    redis \
    && rm -rf /var/lib/apt/lists/*
# I know it's not recomended to start multiple processes in one container,
# but I didn't have time to learn docker compose yet, sorry ._.
CMD sh -c 'redis-server &' && pipenv run python ./main.py

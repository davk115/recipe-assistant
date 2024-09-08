FROM python:3.12-slim

WORKDIR /app

RUN pip install pipenv

COPY data/data_clean.csv data/data_clean.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY recipe_assistant .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 app:app
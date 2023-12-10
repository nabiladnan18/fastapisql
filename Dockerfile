FROM python:3.10-slim

WORKDIR /app

RUN python -m pip install pipenv

COPY Pipfile* .
RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

CMD ["/bin/sh", "-c", "pipenv run alembic upgrade head && pipenv run uvicorn app.main:app --host 0.0.0.0"]
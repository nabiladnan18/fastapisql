FROM python:3.10-slim

WORKDIR /app

RUN python -m pip install pipenv

COPY Pipfile* .
RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
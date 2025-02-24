FROM python:3.13.1-slim

WORKDIR /app/backend

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY requirements /app/backend/requirements/
RUN pip install -r requirements/local.txt

COPY . /app/backend/

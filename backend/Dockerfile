FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt requirements-dev.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt -r /tmp/requirements-dev.txt

COPY . /app
RUN chmod +x /app/scripts/dev.sh

EXPOSE 8000

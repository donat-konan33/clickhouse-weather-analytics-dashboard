FROM python:3.9.20-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pyproject.toml  ./pyproject.toml
COPY ./poetry.lock  ./poetry.lock
COPY ./weatherdashboard  ./weatherdashboard

RUN apt-get update \
    && apt-get -y upgrade \
    && pip3 install --no-cache-dir poetry==2.0.1 \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE $PORT

ENTRYPOINT [ "poetry", "run" ]
CMD ["streamlit", "run", "weatherdashboard/00_dashboard_introduction.py"]

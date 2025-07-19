FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get clean

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]

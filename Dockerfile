FROM python:3.11

RUN mkdir /app && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/RestAPI/src
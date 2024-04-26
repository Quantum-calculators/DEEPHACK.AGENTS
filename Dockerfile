FROM python:3.11

RUN mkdir /app && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/RestAPI/src

# CMD [ "gunicorn main:app -w 9 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000" ]
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

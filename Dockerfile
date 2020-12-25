FROM python:3.8

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--port", "8191", "--host", "0.0.0.0"]
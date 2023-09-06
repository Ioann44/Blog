FROM python:3.10

WORKDIR /app

COPY server/requirements.txt .
RUN pip install -r requirements.txt

COPY server/ .

COPY .env .

CMD ["python", "app.py"]
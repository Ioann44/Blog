FROM python:3.10-alpine

WORKDIR /app

COPY server/ server/
RUN pip install --upgrade pip
RUN pip install -r server/requirements.txt

COPY .env .

CMD ["python", "-u", "server/app.py"]
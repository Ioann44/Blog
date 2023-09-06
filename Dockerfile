FROM python:3.10

WORKDIR /app

COPY server/ server/
RUN pip install -r server/requirements.txt

COPY .env .

CMD ["python", "-u", "server/app.py"]
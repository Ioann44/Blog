FROM python:3.10-alpine

WORKDIR /app

COPY server/requirements.txt server/
RUN pip install --upgrade pip && \
	pip install -r server/requirements.txt

COPY server/ server/
COPY .env .

CMD ["python", "-u", "server/app.py"]
FROM python:3.10-alpine3.15
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

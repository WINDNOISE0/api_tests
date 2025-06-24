FROM python:3.11-slim

WORKDIR /tests

RUN apt-get update

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/tests

ENTRYPOINT ["pytest", "-v", "--tb=short", "--color=yes", "--durations=5"]
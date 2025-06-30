FROM python:3.11-slim

WORKDIR /tests

RUN apt-get update

RUN apt-get update && \
    apt-get install -y curl unzip default-jre && \
    curl -L -o allure.zip https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm -rf allure.zip



COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c", "\
    pytest --alluredir=/tests/allure-results -v --tb=short --color=yes --durations=5 || true; \
    echo 'PYTEST DONE'; \
    ls -la /tests/allure-results; \
    allure generate /tests/allure-results -o /tests/allure-report --clean; \
    echo 'REPORT DONE'; \
    ls -la /tests/allure-report \
"]

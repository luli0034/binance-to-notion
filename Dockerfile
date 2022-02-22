FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && apt-get install zip -y \
    && apt-get install p7zip-full -y

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./src /app

ENTRYPOINT ["python", "main.py"]
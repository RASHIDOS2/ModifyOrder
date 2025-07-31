FROM python:3.11.4

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt ./

COPY . .

RUN /usr/loacl/bin/python -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
    && pip install --no-cache-dir --no-warn-script-location -r requirements.txt

COPY . .
FROM python:3.6.15-bullseye

RUN mkdir -p /home/myapp/weather_project

WORKDIR /home/myapp/weather_project

ENV PYTHONPATH "${PYTHONPATH}:/home/myapp/weather_project"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

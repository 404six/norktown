FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP app
ENV FLASK_ENV development


CMD ["bash", "-c", "flask db init && flask db migrate && flask db upgrade && flask run --host=0.0.0.0"]
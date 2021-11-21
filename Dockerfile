FROM python:3.10-slim

RUN useradd tokei
USER tokei

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY templates/ .
COPY app.py .
CMD [ "gunicorn", "app:app" ]

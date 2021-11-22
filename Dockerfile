FROM python:3.10-slim

RUN useradd -m tokei
USER tokei

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY templates /app/templates
COPY app.py .
COPY gunicorn_config.py .

ENV PATH="/home/tokei/.local/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "-c", "gunicorn_config.py"]

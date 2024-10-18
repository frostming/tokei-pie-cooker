FROM python:3.10-slim as builder

RUN pip install pdm

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY pdm.lock pdm.lock

RUN pdm install -G deploy

FROM python:3.10-slim

RUN useradd -m tokei

COPY --from=builder --chown=tokei:tokei /app/.venv /app/.venv
WORKDIR /app
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_config.py"]

FROM ghcr.io/astral-sh/uv:0.9.3 AS uv

FROM python:3.12.13-slim

COPY --from=uv /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]

FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim AS runner

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"\
    PYTHONPATH=/app/src

COPY --from=builder /opt/venv /opt/venv

COPY src/ /app/src

RUN useradd -m user && chown -R user:user /app
USER user

CMD ["python", "-m", "src.app"]
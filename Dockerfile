#Builder Stage
FROM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


#Runner Stage
FROM python:3.9-slim AS runner

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .
# COPY --from=builder /app .

ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc_dir
RUN mkdir -p $PROMETHEUS_MULTIPROC_DIR

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]
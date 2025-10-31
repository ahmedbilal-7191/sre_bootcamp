#Builder Stage
FROM python:3.9-slim AS Builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .
#Runner Stage
FROM python:3.9-slim AS Runner

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app .

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]
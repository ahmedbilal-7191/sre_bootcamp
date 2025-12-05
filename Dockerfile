#Builder Stage
FROM python:3.12-slim AS builder

WORKDIR /app

# RUN apt-get update && apt-get install --no-install-recommends -y && rm -rf /var/lib/apt/lists/* #this app it doesnt have any system dependencies

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .
#Runner Stage
FROM python:3.12-slim AS runner

RUN useradd --create-home app-runner

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app .
RUN chown -R app-runner:app-runner /app

# COPY . .
USER app-runner

ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc_dir
RUN mkdir -p $PROMETHEUS_MULTIPROC_DIR

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]
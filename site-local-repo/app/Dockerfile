###########
# BUILDER #
###########
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- FIXED: include image and gettext libraries ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc gettext libpq-dev \
    libjpeg-dev zlib1g-dev libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl-dev tk-dev python3-tk && \
    pip install --upgrade pip wheel setuptools && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

#########
# FINAL #
#########
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext libpq5 netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
COPY requirements.txt /app/
RUN pip install --no-cache-dir /wheels/*

COPY --chown=appuser:appuser . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "base.wsgi:application"]

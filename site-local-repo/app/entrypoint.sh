#!/usr/bin/env bash
set -e

echo "🔐 Loading secrets from Docker secrets directory..."

strip_secret() {
    echo -n "$1"   # видаляє \n в кінці
}

load_secret() {
    local name=$1
    local path="/run/secrets/$name"

    if [[ -f "$path" ]]; then
        local raw_value
        raw_value=$(cat "$path")
        export "$name"="$(strip_secret "$raw_value")"
        echo "  ✓ Loaded secret: $name"
    else
        echo "  ⚠ Secret not found: $name"
    fi
}

# Load all secrets created in pipeline
load_secret django_secret_key
load_secret django_debug
load_secret django_allowed_hosts

load_secret postgres_db
load_secret postgres_user
load_secret postgres_password
load_secret db_host
load_secret db_port

load_secret superuser_email
load_secret superuser_password

load_secret gunicorn_workers
load_secret gunicorn_timeout

load_secret email_backend
load_secret smtp_host
load_secret smtp_port
load_secret smtp_user
load_secret smtp_password
load_secret smtp_use_tls
load_secret default_from_email

load_secret stripe_secret_key
load_secret stripe_publishable_key
load_secret stripe_webhook_secret
load_secret stripe_price_id
load_secret site_url

echo "🔧 Exporting environment variables for Django..."

export DJANGO_SECRET_KEY="$(strip_secret "$django_secret_key")"
export DJANGO_DEBUG="$(strip_secret "$django_debug")"
export DJANGO_ALLOWED_HOSTS="$(strip_secret "$django_allowed_hosts")"

export POSTGRES_DB="$(strip_secret "$postgres_db")"
export POSTGRES_USER="$(strip_secret "$postgres_user")"
export POSTGRES_PASSWORD="$(strip_secret "$postgres_password")"
export DB_HOST="$(strip_secret "$db_host")"
export DB_PORT="$(strip_secret "$db_port")"

export DJANGO_SUPERUSER_EMAIL="$(strip_secret "$superuser_email")"
export DJANGO_SUPERUSER_PASSWORD="$(strip_secret "$superuser_password")"

export GUNICORN_WORKERS="$(strip_secret "$gunicorn_workers")"
export GUNICORN_TIMEOUT="$(strip_secret "$gunicorn_timeout")"

export EMAIL_BACKEND="$(strip_secret "$email_backend")"
export SMTP_HOST="$(strip_secret "$smtp_host")"
export SMTP_PORT="$(strip_secret "$smtp_port")"
export SMTP_USER="$(strip_secret "$smtp_user")"
export SMTP_PASSWORD="$(strip_secret "$smtp_password")"
export SMTP_USE_TLS="$(strip_secret "$smtp_use_tls")"
export DEFAULT_FROM_EMAIL="$(strip_secret "$default_from_email")"

export STRIPE_SECRET_KEY="$(strip_secret "$stripe_secret_key")"
export STRIPE_PUBLISHABLE_KEY="$(strip_secret "$stripe_publishable_key")"
export STRIPE_WEBHOOK_SECRET="$(strip_secret "$stripe_webhook_secret")"
export STRIPE_PRICE_ID="$(strip_secret "$stripe_price_id")"
export SITE_URL="$(strip_secret "$site_url")"

# =======================================
# WAIT FOR POSTGRESQL
# =======================================

echo "⏳ Waiting for PostgreSQL..."
until nc -z -v -w30 "$DB_HOST" "$DB_PORT"; do
  echo "   ↪ PostgreSQL not ready yet, sleeping..."
  sleep 1
done

echo "✅ PostgreSQL is up and running!"
echo "🔗 Connected to PostgreSQL at ${DB_HOST}:${DB_PORT}"

# =======================================
# DJANGO SETUP
# =======================================

echo "📦 Running migrations..."
python manage.py makemigrations accounts blog --noinput || true
python manage.py migrate --noinput

echo "🌐 Compiling translations..."
python manage.py compilemessages || echo "No translations found"

echo "🧩 Collecting static files..."
python manage.py collectstatic --noinput
echo "🧩 Static files collected!"

# =======================================
# SUPERUSER
# =======================================

echo "👑 Ensuring superuser exists..."
python manage.py shell <<PY
import os
from django.contrib.auth import get_user_model
User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if email and password:
    user, created = User.objects.get_or_create(email=email)
    user.username = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save()
    print("✅ Superuser created or updated:", email)
else:
    print("⚠ Missing superuser credentials.")
PY

# =======================================
# START GUNICORN
# =======================================

echo "🚀 Starting Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers="${GUNICORN_WORKERS:-3}" \
    --timeout="${GUNICORN_TIMEOUT:-60}" \
    base.wsgi:application

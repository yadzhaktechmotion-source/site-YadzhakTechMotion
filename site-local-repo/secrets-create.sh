#!/usr/bin/env bash
set -e

echo "🚀 Starting secret management script..."

# ===============================
# 1. Enable Docker Swarm
# ===============================
echo "🔍 Checking Swarm status..."
ssh "$PROD_SERVER_USER@$PROD_SERVER_IP" "
  if ! docker info | grep -q 'Swarm: active'; then
    echo '⚠️ Swarm inactive — initializing...'
    docker swarm init
  else
    echo '✅ Swarm already active'
  fi
"

# ===============================
# 2. Remove ALL old secrets
# ===============================
echo "🧹 Removing old Docker secrets..."
ssh "$PROD_SERVER_USER@$PROD_SERVER_IP" '
  for s in $(docker secret ls -q); do
    docker secret rm "$s" >/dev/null 2>&1 || true;
    echo "  - Removed: $s";
  done
'

# ===============================
# 3. Create NEW secrets
# ===============================
echo "📦 Creating new Docker secrets..."

ssh "$PROD_SERVER_USER@$PROD_SERVER_IP" '
  create_secret() {
    name="$1"
    value="$2"
    printf "%s" "$value" | docker secret create "$name" - >/dev/null 2>&1 || true
    echo "  ✓ Secret created: $name"
  }

  # Django Core
  create_secret django_secret_key           "change-me-in-prod"
  create_secret django_debug                "False"
  create_secret django_allowed_hosts        "127.0.0.1,localhost,<srv ip>, yourdomain.com"

  # PostgreSQL
  create_secret postgres_db                 "dockerdjango"
  create_secret postgres_user               "dbuser"
  create_secret postgres_password           "dbpassword"
  create_secret db_host                     "db"
  create_secret db_port                     "5432"

  # Django Superuser
  create_secret superuser_email             "admin@test.com"
  create_secret superuser_password          "admin123"

  # Gunicorn
  create_secret gunicorn_workers            "3"
  create_secret gunicorn_timeout            "60"

  # Email / SMTP
  create_secret email_backend               "django.core.mail.backends.console.EmailBackend"
  create_secret smtp_host                   "smtp.gmail.com"
  create_secret smtp_port                   "587"
  create_secret smtp_user                   "your@gmail.com"
  create_secret smtp_password               "yourpassword"
  create_secret smtp_use_tls                "True"
  create_secret default_from_email          "no-reply@test.com"
  
  create_secret stripe_secret_key         "sk_live_xxx_or_test"
  create_secret stripe_publishable_key    "pk_live_xxx_or_test"
  create_secret stripe_webhook_secret     "whsec_xxx"
  create_secret stripe_price_id           "price_xxx_monthly"   # the recurring Price ID
  create_secret site_url                  "https://yourdomain.com"
'

echo "🎉 All secrets created successfully!"

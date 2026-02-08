# Yadzhak TechMotion Platform

Production-ready Django 5 platform with passwordless authentication, async background jobs, and modern DevOps practices.

This project is designed as a **real-world production reference**, not a demo:
- secure by default
- scalable
- cloud & CI/CD ready

---

##  Features

- Django 5 (modern, secure)
- Passwordless authentication (email verification code)
- Background jobs with Celery + Redis
- Transactional email via Amazon SES (SMTP)
- Docker Swarm deployment
- GitLab CI/CD pipeline
- Secrets management via Docker secrets
- Static & media files via S3 + CloudFront
- Cloudflare protection (WAF, DDoS, rate limits)
- Production-grade security settings

---

##  Architecture (High Level)

User
↓
Cloudflare
↓
Nginx (TLS, security headers)
↓
Django (Gunicorn)
↓
PostgreSQL


Background processing:
Django → Celery → Redis → Amazon SES


Static & media:
S3 → CloudFront → User


See full details in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

##  Security Highlights

- HTTPS everywhere (HSTS enabled)
- Passwordless login (no stored passwords)
- CSRF & secure cookies enabled
- Secrets never stored in Git
- SPF, DKIM, DMARC (BIMI-ready)

See [`docs/SECURITY.md`](docs/SECURITY.md).

---

##  Tech Stack

- **Backend:** Django 5, Python 3.12
- **Async:** Celery, Redis
- **Database:** PostgreSQL
- **Proxy:** Nginx
- **Email:** Amazon SES (SMTP)
- **CI/CD:** GitLab CI
- **Containerization:** Docker, Docker Swarm
- **Cloud:** AWS (EC2, S3, CloudFront)
- **DNS & WAF:** Cloudflare

---

##  Local Development

```bash
cp .env.example .env
docker compose up --build
Apply migrations:

docker compose exec web python manage.py migrate
Create admin user:

docker compose exec web python manage.py createsuperuser
-- Deployment --
Production deploys are handled via GitLab CI/CD

Uses Docker Swarm with rolling updates

Secrets are injected via Docker secrets

See docs/DEPLOYMENT.md.

-- Status Page --
A public /status/ endpoint provides:

Web health

Database connectivity

Background worker status

Email configuration state

-- Roadmap --
Kubernetes (EKS) migration

GitOps with Argo CD

Prometheus & Grafana monitoring

Audit logging

Feature flags

-- License --
MIT

-- Author --
Roman Yadzhak
DevOps / Platform Engineer
Yadzhak TechMotion Inc.

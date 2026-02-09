
---

## docs/ARCHITECTURE.md

```md
# Architecture

This platform is designed with production reliability, security, and scalability in mind.

---

## Components Overview

### Edge
- Cloudflare for DNS, WAF, DDoS protection
- Rate limiting and bot protection

### Reverse Proxy
- Nginx
- TLS termination
- Security headers

### Application
- Django 5
- Gunicorn
- Passwordless authentication

### Background Jobs
- Celery workers
- Redis broker

### Database
- PostgreSQL
- Automated backups recommended

### Email
- Amazon SES via SMTP
- High deliverability configuration

### Static & Media
- S3 for storage
- CloudFront CDN

---

## Deployment Model

- Docker Swarm
- Rolling updates
- Health checks
- Quick rollback

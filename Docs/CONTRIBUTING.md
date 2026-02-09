# Contributing Guide

Thank you for your interest in contributing to **Yadzhak TechMotion Platform**.

This project follows production-grade engineering practices.  
All contributions are expected to maintain **security, reliability, and code quality**.

---

## Contribution Principles

Before contributing, please ensure that your changes:

- Improve clarity, reliability, or security
- Follow existing architecture and patterns
- Are production-ready (no demo shortcuts)
- Do not introduce secrets, credentials, or sensitive data
- Are documented when behavior changes

---

## Development Setup

### Requirements

- Docker
- Docker Compose
- Python 3.12+
- Git

### Local Setup

```bash
git clone https://github.com/<your-org>/<repo>.git
add correct env
start pipeline on GitLab

To get email verification  code >>>
use >>> docker logs -f <container name>
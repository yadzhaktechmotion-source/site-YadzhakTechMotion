# Email Configuration

---

## Provider
- Amazon SES (SMTP)

---

## DNS Records

- SPF: include:amazonses.com
- DKIM: SES-generated CNAME records
- DMARC: quarantine or reject

---

## BIMI

- SVG logo hosted on CDN
- DMARC enforcement required
- Optional VMC/CMC certificate

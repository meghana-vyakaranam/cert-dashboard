# 🔐 CertIntel — Weekly Certificate Intelligence Dashboard

> Tracks TLS/SSL, PKI, certificate lifecycle, and post-quantum cryptography across cloud providers, certificate vendors, and standards organizations. Powered by Claude AI with live web search.

---

## What it does

CertIntel generates a weekly competitive intelligence dashboard for certificate and PKI professionals. Each report is freshly sourced from the web and covers:

- 🚨 **Executive Alerts** — action items requiring immediate attention
- ⏳ **Upcoming Deadlines** — compliance dates and industry milestones
- 📊 **Competitor Landscape** — side-by-side comparison across cloud providers
- ☁️ **Key Moves by Player** — AWS, Azure, GCP, and major vendors
- 🏛️ **Standards & Regulatory Signals** — NIST, CA/Browser Forum, IETF, CISA
- 📈 **Major Trends** — post-quantum, automation, root program changes
- 🧠 **Strategic Takeaways** — executive-level insights
- 🎯 **Recommended Actions** — immediate, near-term, and strategic
- 🗞️ **Full News Dump** — all relevant items with clickable links

---

## Tracked entities

| Category | Entities |
|----------|----------|
| Cloud Providers | AWS, Azure, GCP |
| Certificate Vendors | DigiCert, Sectigo, GlobalSign, GoDaddy |
| Standards & Orgs | NIST, CA/Browser Forum, IETF, CISA, ENISA, CSA |

---

## Tech stack

- **Backend** — Python / Flask
- **AI** — Claude Opus (Anthropic) with live web search
- **Frontend** — Vanilla JS, dark-theme UI with collapsible sections and live streaming

---

## Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your-key-here

# Start the server
python app.py
```

Open [http://localhost:5050](http://localhost:5050) and click **Generate Dashboard**.

---

## Deployment

Deployed on Render. Set `ANTHROPIC_API_KEY` as an environment variable in your hosting platform.

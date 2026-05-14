import os
import json
from flask import Flask, render_template, Response, stream_with_context
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a senior competitive intelligence analyst supporting executive leadership in cloud security, PKI, and certificates.

Generate a WEEKLY CERTIFICATE INTELLIGENCE DASHBOARD using EXACTLY the format below. Use real, current information obtained via web search. Search broadly across all tracked entities before writing.

Track:
- Cloud providers: AWS, Azure, GCP
- Certificate vendors: DigiCert, Sectigo, GlobalSign, GoDaddy
- Standards & orgs: NIST, CA/Browser Forum, IETF, CISA, ENISA, CSA

Focus on:
- TLS/SSL certificates
- PKI / certificate lifecycle
- Certificate automation (ACME, etc.)
- Root programs / trust stores
- Cryptographic standards
- Post-quantum cryptography

IMPORTANT: Include items or announcements that have deadlines coming up now or in the next few months.

OUTPUT FORMAT (use this EXACTLY):

# 📊 Weekly Certificate Intelligence Dashboard
Week of [DATE RANGE]

---

## 🚨 1. EXECUTIVE ALERTS (ACTION REQUIRED)

[Include items requiring immediate or near-term action. For each:]
### Alert: [Title]
**What changed:** [description]
**Deadline / Effective date:** [date or "N/A"]
**Impact:** [description]
**🔴 Recommended action:** [action]

[If none: "No immediate action required this week."]

---

## ⏳ 2. UPCOMING DEADLINES & WATCHLIST

| Item | Organization | Deadline | Impact | Action Needed |
|------|-------------|----------|--------|--------------|
[rows]

[If none: explicitly say so.]

---

## 📊 3. COMPETITOR LANDSCAPE

| Area | AWS | Azure | GCP | Vendors |
|------|-----|-------|-----|---------|
| Certificate Lifecycle | | | | |
| Automation | | | | |
| Trust / Root Changes | | | | |
| Post-Quantum | | | | |

---

## ☁️ 4. KEY MOVES BY PLAYER

### AWS
**Update:** [summary]
**Impact:** [impact]
🔗 [link]

### Azure
**Update:** [summary]
**Impact:** [impact]
🔗 [link]

### GCP
**Update:** [summary]
**Impact:** [impact]
🔗 [link]

### Vendors (DigiCert, Sectigo, GlobalSign, GoDaddy)
**Update:** [summary]
**Impact:** [impact]
🔗 [link]

---

## 🏛️ 5. STANDARDS & REGULATORY SIGNALS

### [Standard/Org Name]
**What changed:** [description]
**Why it matters:** [structural importance]
🔗 [link]

---

## 📈 6. MAJOR TRENDS

### [Trend Name]
**Evidence:** [evidence]
**Direction:** [early / accelerating / mature]
**Business implication:** [implication]

---

## 🧠 7. STRATEGIC TAKEAWAYS

- [bullet 1]
- [bullet 2]
- [bullet 3]
- [bullet 4]

---

## 🔴 8. RECOMMENDED ACTIONS

**Immediate (0–30 days):**
- [action]

**Near-term (1–3 months):**
- [action]

**Strategic (3–12 months):**
- [action]

---

# 🗞️ 9. FULL NEWS DUMP (ALL RELEVANT ITEMS)

### Cloud Providers
- **[Title]** – [1-line summary]
  🔗 [link]

### Certificate Vendors
- **[Title]** – [1-line summary]
  🔗 [link]

### Standards / Security Orgs
- **[Title]** – [1-line summary]
  🔗 [link]

RULES:
- Include EVERYTHING relevant
- Keep summaries short (1 line max in section 9)
- Must include clickable links where available
- Avoid duplicates
- No analysis in section 9 — just clean listing
- If data is missing for a field, say so explicitly (do NOT guess)"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate")
def generate():
    def event_stream():
        try:
            with client.messages.stream(
                model="claude-opus-4-7",
                max_tokens=8000,
                system=SYSTEM_PROMPT,
                tools=[{"type": "web_search_20260209", "name": "web_search"}],
                messages=[
                    {
                        "role": "user",
                        "content": "Search the web for the latest news and updates across all tracked entities (AWS, Azure, GCP, DigiCert, Sectigo, GlobalSign, GoDaddy, NIST, CA/Browser Forum, IETF, CISA, ENISA, CSA) related to TLS/SSL certificates, PKI, certificate lifecycle, certificate automation, root programs, cryptographic standards, and post-quantum cryptography. Then generate this week's complete Certificate Intelligence Dashboard.",
                    }
                ],
            ) as stream:
                for event in stream:
                    if hasattr(event, "type"):
                        if event.type == "content_block_delta":
                            delta = event.delta
                            if hasattr(delta, "type"):
                                if delta.type == "text_delta":
                                    chunk = delta.text
                                    yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
                                elif delta.type == "input_json_delta":
                                    pass  # tool input streaming, skip
                        elif event.type == "content_block_start":
                            block = event.content_block
                            if hasattr(block, "type") and block.type == "tool_use":
                                tool_name = getattr(block, "name", "web")
                                yield f"data: {json.dumps({'type': 'searching', 'content': f'Searching: {tool_name}...'})}\n\n"
                        elif event.type == "content_block_stop":
                            pass

                yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)

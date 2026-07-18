# Minimal Flask CTF Demo

This project is a deliberately vulnerable educational demo for UNSW COMP6441. It is intended only for local demonstrations on localhost and must never be exposed to a public network.

Important: this application contains intentionally insecure code for learning purposes. Do not deploy it publicly or use real credentials.

## Run locally

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000/.

## Challenges

- SQL Injection: /sql-login
- Reflected XSS: /xss?q=hello
- IDOR: /idor?id=2

## Warning

The app is intentionally vulnerable and should only be used on localhost for classroom screenshots and analysis.

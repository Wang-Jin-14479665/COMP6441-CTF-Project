# Testing Guide

## Normal use

1. Start the app with `python app.py`.
2. Open http://127.0.0.1:5000/.
3. Visit the SQL login page and try normal credentials like `alice` / `password123`.
4. Visit the XSS page with a normal query such as `hello`.
5. Visit the IDOR page with `?id=3`.

## Exploitation steps

### SQL injection

1. Open http://127.0.0.1:5000/sql-login.
2. Enter `alice' OR '1'='1` in the username field and any password.
3. Submit the form.
4. The page should display the flag.

### Reflected XSS

1. Open http://127.0.0.1:5000/xss?q=<script>alert('xss')</script>.
2. The script should execute in a normal local browser.

### IDOR

1. Open http://127.0.0.1:5000/idor?id=4.
2. The page should reveal the other fictional profile.

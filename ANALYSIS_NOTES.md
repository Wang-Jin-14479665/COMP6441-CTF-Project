# Analysis Notes

## SQL Injection
- Asset protected: authentication state for the login form.
- Trust boundary: browser input to server-side SQL execution.
- Vulnerable data flow: raw form fields are concatenated into the SQL query.
- Root cause: string interpolation into SQL.
- Attacker assumptions: a crafted username can alter the WHERE clause.
- Exact payload: `alice' OR '1'='1`.
- Expected result: authentication bypass and flag displayed.
- Mitigation: parameterised queries.
- Why it works: the database treats user input as data, not SQL syntax.
- Controls that appear useful but do not fix the root cause: client-side validation, rate limiting, password complexity.
- Security/usability trade-offs: parameterised queries improve security but require careful coding.
- Secrets, type errors, least privilege, insider threats: no secrets are stored; least privilege matters for database accounts; insider misuse is still possible.
- Limitations: this is a simplified demonstration and does not model real password handling.

## Reflected XSS
- Asset protected: the integrity of rendered HTML and the user’s browser context.
- Trust boundary: untrusted query parameter to HTML template output.
- Vulnerable data flow: the search term is inserted directly into the page.
- Root cause: missing output encoding.
- Attacker assumptions: a script payload in the query string will be rendered and executed.
- Exact payload: `<script>alert('xss')</script>`.
- Expected result: the alert executes in a browser.
- Mitigation: escape or encode output before rendering.
- Why it works: the browser sees the payload as text rather than executable HTML.
- Controls that appear useful but do not fix the root cause: hiding the input, using CSP alone, sanitizing after the fact.
- Security/usability trade-offs: encoding protects users but can make some intentionally rich content harder to render.
- Secrets, type errors, least privilege, insider threats: no real secrets are used; the demo is limited to harmless alert execution.
- Limitations: this uses a simple alert to keep the demo deterministic.

## IDOR
- Asset protected: another user’s profile data.
- Trust boundary: the request parameter and the server-side profile lookup.
- Vulnerable data flow: the app trusts the `id` parameter without checking ownership.
- Root cause: missing authorisation check.
- Attacker assumptions: changing the numeric ID will surface another profile.
- Exact payload: `?id=2`.
- Expected result: another fictional profile is revealed.
- Mitigation: enforce ownership checks on the server.
- Why it works: the server rejects requests for records that do not belong to the current user.
- Controls that appear useful but do not fix the root cause: hiding the ID in the UI, changing the URL format.
- Security/usability trade-offs: access checks add complexity but protect data confidentiality.
- Secrets, type errors, least privilege, insider threats: the example uses fictional records; least privilege and insider misuse still matter in real systems.
- Limitations: the demo uses a single current user and a simple numeric ID parameter.

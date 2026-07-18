import sqlite3
from pathlib import Path
from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "demo-secret"
DB_PATH = Path(__file__).with_name("ctf_demo.db")
CURRENT_USER_ID = 1


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            notes TEXT NOT NULL
        )
        """
    )
    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM profiles")
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('users', 'profiles')")
    cur.executemany(
        "INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
        [
            (1, "alice", "password123", "student"),
            (2, "bob", "letmein", "student"),
        ],
    )
    cur.executemany(
        "INSERT INTO profiles (id, owner_id, name, email, notes) VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, "Alice Example", "alice@example.test", "Own profile"),
            (2, 2, "Bob Example", "bob@example.test", "FLAG{idor_missing_authorization}"),
        ],
    )
    conn.commit()
    conn.close()


@app.before_request
def before_request():
    g.db = sqlite3.connect(DB_PATH)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/sql-login", methods=["GET", "POST"])
def sql_login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Vulnerable: intentionally unsafe string concatenation in SQL.
        query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
        row = g.db.execute(query).fetchone()
        if row:
            if "' or '1'='1" in username.lower() or "' or '1'='1" in password.lower():
                message = "Login successful. FLAG{sql_injection_login_bypass}"
            else:
                message = "Login successful."
        else:
            message = "Invalid username or password."
    return render_template("sql_login.html", message=message)


@app.route("/sql-login-secure")
def sql_login_secure():
    return render_template("sql_login_secure.html")


@app.route("/sql-login-secure", methods=["POST"])
def sql_login_secure_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    query = "SELECT id, username, role FROM users WHERE username = ? AND password = ?"
    row = g.db.execute(query, (username, password)).fetchone()
    if row:
        return render_template("sql_login_secure.html", message="Secure login successful.")
    return render_template("sql_login_secure.html", message="Invalid username or password.")


@app.route("/xss")
def xss():
    query = request.args.get("q", "")
    # Vulnerable: reflected input is inserted directly into the HTML.
    if "<script" in query.lower():
        result = "<p>You searched for: " + query + "</p><p>FLAG{xss_untrusted_input}</p>"
    else:
        result = f"<p>You searched for: {query}</p>"
    return render_template("xss.html", query=query, result=result)


@app.route("/xss-secure")
def xss_secure():
    query = request.args.get("q", "")
    return render_template("xss_secure.html", query=query)


@app.route("/idor")
def idor():
    profile_id = request.args.get("id", "1")
    row = g.db.execute("SELECT id, owner_id, name, email, notes FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    if row is None:
        return render_template("idor.html", profile=None, message="Profile not found.")
    profile = {
        "id": row[0],
        "owner_id": row[1],
        "name": row[2],
        "email": row[3],
        "notes": row[4],
    }
    return render_template("idor.html", profile=profile, message="")


@app.route("/idor-secure")
def idor_secure():
    profile_id = request.args.get("id", "1")
    row = g.db.execute("SELECT id, owner_id, name, email, notes FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    if row is None:
        return render_template("idor.html", profile=None, message="Profile not found.")
    if row[1] != CURRENT_USER_ID:
        return render_template("idor.html", profile=None, message="Access denied.")
    profile = {
        "id": row[0],
        "owner_id": row[1],
        "name": row[2],
        "email": row[3],
        "notes": row[4],
    }
    return render_template("idor.html", profile=profile, message="")


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)

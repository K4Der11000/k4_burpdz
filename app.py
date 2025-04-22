from flask import Flask, request, render_template, redirect, url_for, session, jsonify, render_template_string
import threading, time, os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['results'] = []
app.config['status'] = 'Idle'

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'static'] and 'logged_in' not in session:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'kader11000':
            session['logged_in'] = True
            return redirect('/')
        else:
            return "Wrong credentials", 401

    return render_template_string('''
    <html><body style="background-color:#0d1117; color:white; font-family:monospace;">
        <h2>Login</h2>
        <form method="POST">
            <label>Username:</label><input name="username"><br>
            <label>Password:</label><input name="password" type="password"><br>
            <button type="submit">Login</button>
        </form>
    </body></html>
    ''')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/')
def index():
    return render_template("index.html", last_url='', request_template='', status=app.config['status'])

@app.route('/api/status')
def api_status():
    return jsonify({
        "results": app.config.get("results", []),
        "status": app.config.get("status", "Idle")
    })

if __name__ == '__main__':
    app.run(debug=True)

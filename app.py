from flask import Flask, render_template_string, request, jsonify, send_from_directory, redirect, session import re import requests import os from datetime import datetime

app = Flask(name) app.secret_key = "any_random_secret_key" PASSWORD = "kader11000"

LOGIN_PAGE = '''

<form method="POST" style="margin:100px auto;width:300px;background:#000;color:#0ff;padding:20px;border:1px solid #0ff;border-radius:10px;font-family:monospace">
  <h2>Enter Password</h2>
  <input type="password" name="password" style="width:100%;margin:10px 0;padding:8px;border-radius:5px;background:#111;color:#0ff">
  <button type="submit" style="width:100%;padding:8px;background:#0ff;color:#000;border:none;border-radius:5px">Login</button>
</form>
'''HTML_TEMPLATE = '''

<!DOCTYPE html><html>
<head>
  <title>Fuzzing Tool</title>
  <style>
    body { background:#000; color:#0ff; font-family:monospace; margin:0; padding:0; }
    .hacker-banner {
      background: linear-gradient(-45deg, #111, #0f0, #00f, #111);
      background-size: 400% 400%;
      animation: animateBG 8s ease infinite;
      color: #0ff;
      padding: 15px;
      text-align: center;
      position: relative;
      border-bottom: 2px solid #0ff;
    }
    .hacker-banner h1 { margin: 0; font-size: 28px; color: #0ff; }
    .hacker-banner span { color: #ff0; text-shadow: 0 0 5px #ff0; }
    @keyframes animateBG {
      0% {background-position: 0% 50%;}
      50% {background-position: 100% 50%;}
      100% {background-position: 0% 50%;}
    }
    textarea, input[type=text] { width: 100%; background:#111; color:#0ff; border:1px solid #0ff; padding:5px; margin-top:5px; }
    iframe { width: 100%; height: 400px; border:1px solid #0ff; margin-top: 10px; }
    #terminal { background:#111; color:#0f0; padding:10px; height:200px; overflow:auto; border:1px solid #0f0; }
    button { background:#0ff; color:#000; border:none; padding:10px; margin:10px 0; cursor:pointer; }
  </style>
</head>
<body>
<div class="hacker-banner">
  <h1>Welcome, <span>kader11000</span></h1>
  <img src="https://img.icons8.com/ios-filled/50/0ff/hacker.png" style="position:absolute;top:10px;left:10px;height:30px;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_Algeria.svg" style="position:absolute;top:10px;right:10px;height:30px;border-radius:5px;">
</div>
<a href="/logout" style="position:absolute;top:15px;left:15px;color:#f00;border:1px solid #f00;padding:5px 10px;border-radius:5px;text-decoration:none">Logout</a>
<div style="padding:20px">
  <form onsubmit="startFuzzing(event)">
    <label>Target URL:</label>
    <input type="text" id="url" required>
    <label>Request Template (use {{region}} for fuzzing):</label>
    <textarea id="request" rows="6"></textarea>
    <label>Wordlist (comma separated):</label>
    <input type="text" id="wordlist">
    <label>Keyword to detect success:</label>
    <input type="text" id="keyword">
    <button type="submit">Start Fuzzing</button>
  </form>
  <iframe id="resultFrame"></iframe>
  <div id="terminal"></div>
</div>
<audio id="start-audio" src="/static/start.mp3" preload="auto"></audio>
<audio id="fail-audio" src="/static/fail.mp3" preload="auto"></audio>
<audio id="success-audio" src="/static/success.mp3" preload="auto"></audio>
<script>
function startFuzzing(e) {
  e.preventDefault();
  const form = new FormData();
  form.append("url", document.getElementById("url").value);
  form.append("request", document.getElementById("request").value);
  form.append("wordlist", document.getElementById("wordlist").value);
  form.append("keyword", document.getElementById("keyword").value);
  document.getElementById("start-audio").play();fetch("/fuzz", { method: "POST", body: form }) .then(res => res.json()) .then(data => { document.getElementById("terminal").innerText = data.log.join("\n"); if (data.match) { document.getElementById("resultFrame").srcdoc = data.response; document.getElementById("success-audio").play(); alert("Keyword matched! Result shown."); } else { document.getElementById("fail-audio").play(); alert("No match found."); } }); } </script>

</body>
</html>
'''@app.route("/", methods=["GET", "POST"]) def index(): if request.method == "POST": if request.form.get("password") == PASSWORD: session["authenticated"] = True return redirect("/") else: return render_template_string("<h2 style='color:red'>Wrong password</h2>" + LOGIN_PAGE)

if not session.get("authenticated"):
    return render_template_string(LOGIN_PAGE)

return render_template_string(HTML_TEMPLATE)

@app.route("/logout") def logout(): session.clear() return redirect("/")

@app.route("/fuzz", methods=["POST"]) def fuzz(): url = request.form['url'] raw_request = request.form['request'] keyword = request.form['keyword'] wordlist = request.form['wordlist'].split(',')

regions = re.findall(r"{{(.*?)}}", raw_request)
logs = [f"Starting fuzzing with regions: {regions}"]

from itertools import product
combos = list(product(wordlist, repeat=len(regions)))
for combo in combos:
    fuzzed = raw_request
    for region, word in zip(regions, combo):
        fuzzed = fuzzed.replace("{{" + region + "}}", word)

    try:
        request_lines = fuzzed.strip().split("\n")
        if len(request_lines[0].split()) < 2:
            logs.append("Invalid request line")
            continue
        method, path, *_ = request_lines[0].split()
        headers = {}
        data = ""
        in_headers = True
        for line in request_lines[1:]:
            if line.strip() == "":
                in_headers = False
                continue
            if in_headers and ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
            else:
                data += line + "\n"

        full_url = url + path if path.startswith('/') else path
        resp = requests.request(method, full_url, headers=headers, data=data.strip(), timeout=5)
        logs.append(f"Tried: {combo} - Status: {resp.status_code}")

        if keyword in resp.text:
            logs.append(f"Match found with {combo}")
            os.makedirs("results", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"success_{timestamp}.html"
            result_path = os.path.join("results", filename)
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(f"<html><body style='background:#000;color:#0f0;font-family:monospace'>")
                f.write(f"<h2>Match Found</h2>")
                f.write(f"<p><b>URL:</b> {full_url}</p>")
                f.write(f"<p><b>Keyword:</b> {keyword}</p>")
                f.write(f"<pre>{fuzzed}</pre>")
                f.write(f"<hr><pre>{resp.text}</pre>")
                f.write("</body></html>")

            return jsonify(match=True, response=resp.text, log=logs, filename=filename)

    except Exception as e:
        logs.append(f"Error with {combo}: {e}")

return jsonify(match=False, log=logs)

@app.route("/download") def download(): filename = request.args.get("filename") return send_from_directory("results", filename, as_attachment=True)

@app.route("/archive") def archive(): files = os.listdir("results") date_filter = request.args.get("date") if date_filter: date_prefix = date_filter.replace('-', '') files = [f for f in files if f.startswith(f"success_{date_prefix}") and f.endswith(".html")] else: files = [f for f in files if f.endswith(".html")] files = sorted(files) return jsonify(files)

if name == "main": app.run(debug=True)


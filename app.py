from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

with open("proxy_config.json") as f:
    proxies_config = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    content = ""
    status = ""
    selected_region = request.form.get("region", "India")
    url = request.form.get("url", "")
    if request.method == "POST" and url:
        proxies = proxies_config.get(selected_region, {})
        try:
            resp = requests.get(url, proxies=proxies, timeout=10)
            content = resp.text
            status = f"Status: {resp.status_code}"
        except Exception as e:
            content = str(e)
            status = "Failed to fetch URL."
    return render_template("index.html", regions=list(proxies_config.keys()), selected_region=selected_region,
                           url=url, content=content, status=status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

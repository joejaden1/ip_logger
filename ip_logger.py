from flask import Flask, request, render_template_string
import requests
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "log.txt"

def get_client_ip():
    # Check for X-Forwarded-For header first
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    # Then check for X-Real-IP header
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    # Finally, fall back to remote_addr
    return request.remote_addr

def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            pass

@app.route('/')
def get_ip_info():
    try:
        user_ip = get_client_ip()
        response = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=5)
        response.raise_for_status()
        data = response.json()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{now}] {user_ip} - {data.get('city', 'N/A')}, {data.get('country', 'N/A')} - {data.get('isp', 'N/A')}\n"

        ensure_log_file()
        with open(LOG_FILE, "a") as log:
            log.write(log_line)
        
        return render_template_string("""
            <h1>IP Information</h1>
            <p>IP: {{ ip }}</p>
            <p>City: {{ city }}</p>
            <p>Country: {{ country }}</p>
            <p>ISP: {{ isp }}</p>
            <p><a href="/logs">View all visits</a></p>
        """, 
        ip=user_ip,
        city=data.get('city', 'N/A'),
        country=data.get('country', 'N/A'),
        isp=data.get('isp', 'N/A'))

    except requests.RequestException as e:
        return f"<h1>Error</h1><p>Failed to fetch IP information: {str(e)}</p>", 500
    except Exception as e:
        return f"<h1>Error</h1><p>An unexpected error occurred: {str(e)}</p>", 500

@app.route('/logs')
def show_logs():
    try:
        ensure_log_file()
        with open(LOG_FILE, "r") as log:
            content = log.read().replace('\n', '<br>')
        return render_template_string("""
            <h2>Visit History</h2>
            <p>{{ content|safe }}</p>
            <p><a href="/">Back to IP lookup</a></p>
        """, content=content)
    except Exception as e:
        return f"<h1>Error</h1><p>Failed to read logs: {str(e)}</p>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

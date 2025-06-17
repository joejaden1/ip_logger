from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def get_ip_info():
    try:
        user_ip = request.remote_addr
        response = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=5).json()  

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Fix: API response keys are lowercase
        log_line = f"[{now}] {user_ip} - {response.get('city', 'N/A')}, {response.get('country', 'N/A')} - {response.get('isp', 'N/A')}\n"

        with open("log.txt", "a") as log:
            log.write(log_line)
        
        return f"""
            <h1>Done!</h1>
            <p>IP: {user_ip}</p>
            <p>City: {response.get('city', 'N/A')}</p>
            <p>Country: {response.get('country', 'N/A')}</p>
            <p>ISP: {response.get('isp', 'N/A')}</p>
        """
    except requests.RequestException as e:
        return f"<h1>Error</h1><p>Failed to fetch IP information: {str(e)}</p>", 500
    except Exception as e:
        return f"<h1>Error</h1><p>An unexpected error occurred: {str(e)}</p>", 500

# Fix: Add route decorator for show_logs
@app.route('/logs')
def show_logs():
    try:
        with open("log.txt", "r") as log:
            content = log.read().replace('\n', '<br>')
        return f"<h2>Visits:</h2><p>{content}</p>"
    except FileNotFoundError:
        return "<h2>Visits:</h2><p>No visits recorded yet.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

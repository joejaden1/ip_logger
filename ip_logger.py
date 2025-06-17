from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def get_ip_info():
    user_ip = request.remote_addr
    response = requests.get(f"http://ip-api.com/json/{user_ip}").json()  

    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {user_ip} - {response.get('city', 'N/A')}, {response.get('country', 'N/A')} - {response.get('isp', 'N/A')}\n"

    with open("log.txt", "a") as log:
        log.write(log_line)
    
    return f"""
        <h1>Done!</h1>
        <p>IP: {user_ip}</p>
        <p>City: {response.get('City', 'N/A')}</p>
        <p>Country: {response.get('Country', 'N/A')}</p>
        <p>ISP: {response.get('ISP', 'N/A')}</p>
    """
def show_logs():
    try:
        with open("log.txt", "r") as log:
            content = log.read().replace('\n', '<br<')
        return f"<h2> visites: </h2><p>{content}</p>"
    except FileNotFoundError:
        return "<p>vistis count:</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

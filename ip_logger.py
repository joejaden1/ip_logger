from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def get_ip_info():
    user_ip = request.remote_addr
    response = requests.get(f"http://ip-api.com/json/{user_ip}").json()  
    
    return f"""
        <h1>Done!</h1>
        <p>IP: {user_ip}</p>
        <p>City: {response.get('city', 'N/A')}</p>
        <p>Country: {response.get('country', 'N/A')}</p>
        <p>ISP: {response.get('isp', 'N/A')}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

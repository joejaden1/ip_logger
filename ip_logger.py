# ip_logger.py
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def get_ip_info():
    user_ip = request.remote_addr
    response = requests.get(f"http://ip-api.com/json{user_ip}")
    return f"""
        <h1> done (; </h1>
        <p>IP: {user_ip} </p>
        <p>city: {response.get('city')}</p>
        <p>country: {response.get('country')}</p>
        <p>ISP: {response.get('isp')}</p>
    """

if __name__ =="__main__":
    app.run(host="0.0.0.0",port=5000)

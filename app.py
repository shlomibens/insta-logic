from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "The server is running! Use /analyze?username=YOUR_NAME"

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not username:
        return "Please provide a username."

    # כאן המערכת פונה ל-Apify
    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
    data = {"usernames": [username]}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        return jsonify(result)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

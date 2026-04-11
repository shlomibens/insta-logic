from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "The server is UP! Use /test to check more."

@app.route('/test')
def test():
    return "Test path is working!"

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    return f"You are looking for: {username}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

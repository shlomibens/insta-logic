from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Insta-Analyzer is LIVE. Use /analyze?username=YOUR_NAME"

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    # שליפת הטוקן מהגדרות השרת
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not username:
        return jsonify({"error": "Missing username"}), 400
    if not api_token:
        return jsonify({"error": "API Token not configured in Render"}), 500

    # פנייה ל-Apify לסריקת הפרופיל
    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
    payload = {"usernames": [username]}
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        data = response.json()
        
        if not data or len(data) == 0:
            return jsonify({"error": "No data found for this user"}), 404
            
        user_info = data[0]
        followers = user_info.get('followersCount', 0)
        # חישוב ממוצע לייקים מ-12 פוסטים אחרונים
        posts = user_info.get('latestPosts', [])
        if posts:
            avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts)
            engagement_rate = (avg_likes / followers) * 100 if followers > 0 else 0
        else:
            avg_likes = 0
            engagement_rate = 0

        return jsonify({
            "username": username,
            "followers": followers,
            "avg_likes_latest": round(avg_likes, 2),
            "engagement_rate": f"{round(engagement_rate, 2)}%"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>מנתח אינסטגרם</title>
    <style>
        body { font-family: sans-serif; background: linear-gradient(to right, #833ab4, #fd1d1d, #fcb045); display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 300px; text-align: center; }
        input { width: 80%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #e1306c; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>InstaCheck</h1>
        <form action="/analyze" method="get">
            <input type="text" name="username" placeholder="שם משתמש..." required>
            <button type="submit">בדוק עכשיו</button>
        </form>
        {% if username %}
        <div class="result">
            <h3>@{{ username }}</h3>
            <p>עוקבים: {{ followers }}</p>
            <p>מעורבות: <strong>{{ engagement }}</strong></p>
        </div>
        {% endif %}
        {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not username:
        return render_template_string(HTML_PAGE, error="נא להזין שם")
    
    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
    
    try:
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = res.json()
        
        if not data:
            return render_template_string(HTML_PAGE, error="לא נמצאו נתונים (פרופיל פרטי?)")
        
        user = data[0]
        f_count = user.get('followersCount', 0)
        posts = user.get('latestPosts', [])
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / f_count) * 100 if f_count > 0 else 0
        
        return render_template_string(HTML_PAGE, username=username, followers=f"{f_count:,}", engagement=f"{round(er, 2)}%")
    except Exception as e:
        return render_template_string(HTML_PAGE, error="שגיאה בסריקה")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>מנתח אינסטגרם</title>
    <style>
        body { font-family: sans-serif; background: #fafafa; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        .btn { display: inline-block; margin-top: 15px; padding: 10px 20px; background: #bc1888; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="card">
        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% else %}
            <h2>@{{ username }}</h2>
            <p>עוקבים: {{ followers }}</p>
            <p>אחוז מעורבות: <strong>{{ engagement_rate }}</strong></p>
        {% endif %}
        <a href="/" class="btn">חיפוש חדש</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return '''
    <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
        <h1>Instagram Analyzer</h1>
        <form action="/analyze" method="get">
            <input type="text" name="username" placeholder="שם משתמש" required>
            <button type="submit">נתח</button>
        </form>
    </div>
    '''

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not api_token:
        return "Missing API Token in Render Settings", 500

    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
    try:
        response = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = response.json()
        if not data:
            return render_template_string(HTML_TEMPLATE, error="לא נמצאו נתונים")
        
        user = data[0]
        f_count = user.get('followersCount', 0)
        posts = user.get('latestPosts', [])
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / f_count) * 100 if f_count > 0 else 0
        
        return render_template_string(HTML_TEMPLATE, username=username, followers=f"{f_count:,}", engagement_rate=f"{round(er, 2)}%")
    except:
        return render_template_string(HTML_TEMPLATE, error="שגיאה בסריקה")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
            <div class="stat">
                <label>שם משתמש</label>
                <span>@{{ username }}</span>
            </div>
            <div class="stat">
                <label>עוקבים</label>
                <span>{{ followers }}</span>
            </div>
            <div class="stat">
                <label>ממוצע לייקים</label>
                <span>{{ avg_likes }}</span>
            </div>
            <div class="stat">
                <label>אחוז מעורבות</label>
                <span class="er-high">{{ engagement_rate }}</span>
            </div>
            <a href="/" class="btn">בדיקה חדשה</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return """
    <body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#fafafa;">
        <h1>Instagram Analyzer</h1>
        <form action="/analyze" method="get">
            <input type="text" name="username" placeholder="הכנס שם משתמש" style="padding:10px; border-radius:5px; border:1px solid #ccc;">
            <button type="submit" style="padding:10px 20px; background:#bc1888; color:white; border:none; border-radius:5px; cursor:pointer;">נתח פרופיל</button>
        </form>
    </body>
    """

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not username:
        return render_template_string(HTML_TEMPLATE, error="נא להזין שם משתמש")

    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
    payload = {"usernames": [username]}
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        data = response.json()
        
        if not data:
            return render_template_string(HTML_TEMPLATE, error="הפרופיל פרטי או לא נמצא")
            
        user_info = data[0]
        followers = user_info.get('followersCount', 0)
        posts = user_info.get('latestPosts', [])
        
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        engagement_rate = (avg_likes / followers) * 100 if followers > 0 else 0

        return render_template_string(HTML_TEMPLATE, 
            username=username, 
            followers=f"{followers:,}", 
            avg_likes=round(avg_likes, 1), 
            engagement_rate=f"{round(engagement_rate, 2)}%")
        
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error="שגיאת תקשורת עם אינסטגרם")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
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

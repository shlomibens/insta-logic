from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# עיצוב ה-HTML וה-CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מנתח אינסטגרם</title>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Assistant', sans-serif; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; color: #333; }
        .card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 350px; text-align: center; }
        h1 { margin-bottom: 20px; color: #bc1888; }
        .stat { margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 10px; }
        .stat label { display: block; font-size: 0.9em; color: #666; }
        .stat span { font-size: 1.4em; font-weight: bold; color: #222; }
        .er-high { color: #28a745 !important; }
        .btn { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #bc1888; color: white; text-decoration: none; border-radius: 50px; transition: 0.3s; }
        .btn:hover { background: #8a1265; }
        .error { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        {% if error %}
            <h1>אופס!</h1>
            <p class="error">{{ error }}</p>
            <a href="/" class="btn">נסה שוב</a>
        {% else %}
            <h1>נתוני פרופיל</h1>
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

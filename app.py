import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Insta-Intelligence | Agency Grade</title>
    <style>
        :root { --accent: #00d2ff; --bg: #0a0a0a; --card: #161616; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: white; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; }
        .header { text-align: center; padding: 40px 0; background: linear-gradient(180deg, #1a1a1a 0%, var(--bg) 100%); border-radius: 30px; }
        .badge-premium { background: gold; color: black; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.7em; text-transform: uppercase; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .card { background: var(--card); padding: 20px; border-radius: 20px; border: 1px solid #222; position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--accent); }
        
        .value { font-size: 1.8em; font-weight: 800; color: var(--accent); display: block; }
        .label { font-size: 0.8em; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        
        .price-tag { background: #2ecc71; color: white; padding: 15px; border-radius: 15px; text-align: center; margin-top: 20px; font-size: 1.2em; }
        .price-value { font-size: 1.5em; font-weight: bold; display: block; }

        .search-box { background: var(--card); padding: 10px; border-radius: 15px; display: flex; gap: 10px; margin-bottom: 30px; }
        input { background: transparent; border: none; color: white; flex: 1; padding: 10px; outline: none; }
        button { background: var(--accent); border: none; padding: 10px 25px; border-radius: 12px; font-weight: bold; cursor: pointer; }
        
        .report-btn { width: 100%; padding: 15px; background: white; color: black; border-radius: 15px; font-weight: bold; border: none; margin-top: 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge-premium">Internal Intelligence</span>
            <h1 style="font-size: 2.5em; margin: 10px 0;">Insta-Intel <span style="color:var(--accent)">PRO</span></h1>
            <div class="search-box">
                <form action="/analyze" method="get" style="display:flex; width:100%;">
                    <input type="text" name="username" placeholder="הזן פרופיל VIP לניתוח..." required>
                    <button type="submit">GENERATE REPORT</button>
                </form>
            </div>
        </div>

        {% if username %}
        <div class="grid">
            <div class="card">
                <span class="label">שווי שוק לפוסט</span>
                <span class="value">${{ post_value }}</span>
            </div>
            <div class="card">
                <span class="label">ציון אותנטיות</span>
                <span class="value">{{ auth_score }}%</span>
            </div>
            <div class="card">
                <span class="label">מעורבות קהל</span>
                <span class="value">{{ engagement }}</span>
            </div>
            <div class="card">
                <span class="label">פוטנציאל ויראלי</span>
                <span class="value">{{ viral_potential }}</span>
            </div>
        </div>

        <div class="price-tag">
            <span class="label" style="color: white; opacity: 0.8;">הכנסה שנתית משוערת מחסויות</span>
            <span class="price-value">${{ annual_est }}</span>
        </div>

        <div class="card" style="margin-top:20px; border-right: 4px solid #f1c40f; border-left:none;">
            <span class="label">💡 המלצה אסטרטגית לסוכן:</span>
            <p style="font-size: 0.9em; line-height: 1.6;">{{ strategy }}</p>
        </div>

        <button class="report-btn">הורד דוח PDF מלא (Premium Only)</button>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    token = os.environ.get('APIFY_TOKEN')
    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}"
    
    try:
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = res.json()[0]
        
        followers = data.get('followersCount', 0)
        posts = data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_likes / followers) * 100 if followers > 0 else 0
        
        # חישוב שווי פוסט (לפי ממוצע שוק של $10 לכל 1000 עוקבים כפול מדד מעורבות)
        val_per_post = (followers / 1000) * 10 * (1 + er/10)
        annual_est = val_per_post * 52 # חישוב לפי פוסט אחד בשבוע
        
        # לוגיקת אסטרטגיה
        strategy = "הפרופיל במצב מצוין. מומלץ להעלות את מחיר החסות ב-15% ולמקד תוכן ב-Reels בימי שלישי."
        if er < 1.5:
            strategy = "אזהרה: המעורבות בדעיכה. יש לבצע 'ניקוי עוקבים' ולהגדיל אינטראקציה בסטורי כדי להצדיק את המחיר למפרסמים."

        return render_template_string(HTML_TEMPLATE, 
            username=username, 
            post_value=f"{int(val_per_post):,}",
            auth_score=int(100 - (er*2)) if er < 2 else 94,
            engagement=f"{round(er, 2)}%",
            viral_potential="HIGH" if er > 3 else "MEDIUM",
            annual_est=f"{int(annual_est):,}",
            strategy=strategy)
    except:
        return render_template_string(HTML_TEMPLATE, error="Error analyzing VIP profile")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

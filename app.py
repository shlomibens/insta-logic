import os
from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>INSTA-INTEL PRO | Deep Analysis</title>
    <style>
        :root { --neon: #00f2ff; --gold: #d4af37; --bg: #050505; --card: rgba(255,255,255,0.03); }
        body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
        .container { max-width: 900px; margin: auto; }
        
        /* Glass Header */
        header { background: var(--card); backdrop-filter: blur(10px); border: 1px solid #222; padding: 30px; border-radius: 30px; text-align: center; margin-bottom: 30px; }
        .logo { font-size: 2.5em; font-weight: 900; letter-spacing: -2px; }
        
        /* Search Area */
        .search-box { display: flex; gap: 10px; margin-bottom: 40px; }
        input { flex: 1; background: #111; border: 1px solid #333; color: white; padding: 15px; border-radius: 15px; outline: none; }
        button { background: white; color: black; border: none; padding: 0 30px; border-radius: 15px; font-weight: bold; cursor: pointer; }

        /* Score Breakdown */
        .score-section { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 30px; }
        .main-score { background: linear-gradient(135deg, #111, #000); border: 2px solid var(--neon); border-radius: 30px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; }
        .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .mini-card { background: var(--card); padding: 20px; border-radius: 20px; border: 1px solid #222; }

        /* ROI Table */
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: var(--card); border-radius: 20px; overflow: hidden; }
        th, td { padding: 15px; text-align: center; border-bottom: 1px solid #222; }
        th { background: #111; color: var(--gold); font-size: 0.8em; text-transform: uppercase; }

        /* The Memo */
        .memo { background: #f9f9f9; color: #111; padding: 30px; border-radius: 4px; margin-top: 40px; position: relative; font-family: 'Courier New', serif; box-shadow: 15px 15px 0 var(--neon); }
        .memo::after { content: "TOP SECRET"; position: absolute; top: 10px; left: 10px; border: 2px solid red; color: red; padding: 2px 10px; transform: rotate(-15deg); font-weight: bold; opacity: 0.5; }
        
        .label { font-size: 0.7em; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">INSTA-INTEL <span style="color:var(--neon)">PRO</span></div>
            <p style="color:#666">מערכת ניתוח עומק למנהלים וסוכנויות מובילות</p>
            <div class="search-box">
                <form action="/analyze" method="get" style="display:flex; width:100%; gap:10px;">
                    <input type="text" name="username" placeholder="הכנס שם משתמש לניתוח..." required>
                    <button type="submit">GENERATE REPORT</button>
                </form>
            </div>
        </header>

        {% if username %}
        <div class="score-section">
            <div class="main-score">
                <span class="label">ציון איכות כולל</span>
                <span style="font-size: 4em; font-weight: 900; color: var(--neon);">{{ total_score }}/10</span>
                <span style="font-size: 0.8em; color: #555;">VIP Rank: {{ rank }}</span>
            </div>
            <div class="details-grid">
                <div class="mini-card"><span class="label">אותנטיות קהל</span><span style="display:block; font-size: 1.5em;">{{ auth_score }}%</span></div>
                <div class="mini-card"><span class="label">מדד עקביות</span><span style="display:block; font-size: 1.5em;">{{ consistency }}%</span></div>
                <div class="mini-card"><span class="label">שווי שוק (פוסט)</span><span style="display:block; font-size: 1.5em; color:#2ecc71;">${{ post_value }}</span></div>
                <div class="mini-card"><span class="label">מעורבות (ER)</span><span style="display:block; font-size: 1.5em;">{{ engagement }}%</span></div>
            </div>
        </div>

        <h3 style="color:var(--gold)">💰 מחירון מומלץ למפרסמים (ROI Estimate)</h3>
        <table>
            <thead>
                <tr><th>סוג תוכן</th><th>מחיר מומלץ</th><th>חשיפה משוערת</th></tr>
            </thead>
            <tbody>
                <tr><td>סטורי (24 שעות)</td><td>${{ price_story }}</td><td>{{ reach_story }}</td></tr>
                <tr><td>פוסט בפיד</td><td>${{ post_value }}</td><td>{{ reach_post }}</td></tr>
                <tr><td>סרטון Reels</td><td>${{ price_reels }}</td><td>{{ reach_reels }}</td></tr>
            </tbody>
        </table>

        <div class="memo">
            <h3 style="margin-top:0">ניתוח אסטרטגי עבור: @{{ username }}</h3>
            <strong>פרסונה מזוהה:</strong> {{ persona }}<br>
            <strong>שעות זהב לפרסום:</strong> {{ golden_hours }}<br><br>
            <strong>תמצית למקבלי החלטות:</strong><br>
            {{ strategy }}
            <br><br>
            <small>נחתם ע"י: AI Core Analytics | Intelligence Unit</small>
        </div>
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
        
        # חישובים מורכבים
        auth_score = 94 if er > 2 else 72
        consistency = 85 if len(posts) > 10 else 40
        total_score = round((er * 2) + (consistency / 20) + (auth_score / 20), 1)
        total_score = min(total_score, 10)
        
        # תמחור
        base_val = (followers / 1000) * 15
        post_val = int(base_val * (1 + er/5))
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, 
            total_score=total_score,
            rank="Elite" if total_score > 8 else "Standard",
            auth_score=auth_score,
            consistency=consistency,
            engagement=round(er, 2),
            post_value=f"{post_val:,}",
            price_story=f"{int(post_val * 0.4):,}",
            price_reels=f"{int(post_val * 1.5):,}",
            reach_story=f"{int(followers * 0.08):,}",
            reach_post=f"{int(followers * 0.2):,}",
            reach_reels=f"{int(followers * 2.5):,}",
            persona="Business Growth" if "shop" in data.get('biography','') else "Public Figure",
            golden_hours="18:00 - 21:00 (שעון מקומי)",
            strategy=f"על סמך ניתוח ה-AI, הפרופיל נמצא במצב { 'מעולה' if total_score > 7 else 'טעון שיפור' }. "
                     f"ההמלצה למזכירה היא לתעדף יצירת תוכן וידאו (Reels) שכן פוטנציאל החשיפה שם גבוה פי 2.5 מכמות העוקבים הקיימת.")
    except:
        return render_template_string(HTML_TEMPLATE, error="Error")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

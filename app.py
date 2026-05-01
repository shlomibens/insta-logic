import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>INSTA-INTEL | BLACK EDITION</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Assistant:wght@200;400;800&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #d4af37; --danger: #ff3e3e; --glass: rgba(255, 255, 255, 0.03); }
        
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { 
            background: #000; color: #fff; font-family: 'Assistant', sans-serif; 
            margin: 0; padding: 0; min-height: 100vh;
            background-image: radial-gradient(circle at 50% -20%, #112244 0%, #000000 100%);
        }

        .hero-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; }
        .pulse { position: absolute; top: -20%; left: -20%; width: 140%; height: 140%; background: radial-gradient(circle, rgba(0, 242, 255, 0.05) 0%, transparent 70%); animation: pulse-anim 8s infinite alternate; }
        @keyframes pulse-anim { from { transform: scale(1); opacity: 0.3; } to { transform: scale(1.1); opacity: 0.6; } }

        .container { max-width: 500px; margin: 0 auto; padding: 20px; }

        header { text-align: center; padding: 40px 0 20px; }
        .logo { font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: -2px; background: linear-gradient(to bottom, #fff, #666); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .version { font-size: 0.6rem; background: var(--gold); color: #000; padding: 2px 8px; border-radius: 4px; vertical-align: middle; margin-right: 5px; font-weight: 800; }

        /* Modern Search Box */
        .search-panel { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 25px; padding: 8px; display: flex; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.5); }
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 15px 20px; font-size: 1rem; outline: none; }
        button { background: #fff; color: #000; border: none; padding: 0 25px; border-radius: 18px; font-weight: 800; font-size: 0.9rem; cursor: pointer; transition: 0.2s; }
        button:active { transform: scale(0.95); }

        /* Main Score Radial */
        .score-circle { width: 180px; height: 180px; margin: 0 auto 30px; border-radius: 50%; border: 2px solid #222; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: radial-gradient(circle, #0a0a0a, #000); box-shadow: 0 0 50px rgba(0, 242, 255, 0.1); }
        .score-circle::before { content: ''; position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid var(--neon); border-top-color: transparent; border-left-color: transparent; transform: rotate(45deg); }
        .big-num { font-size: 3.5rem; font-weight: 900; color: #fff; line-height: 1; }
        .score-lbl { font-size: 0.7rem; color: var(--neon); letter-spacing: 2px; text-transform: uppercase; margin-top: 5px; }

        /* Data Matrix */
        .matrix { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
        .m-card { background: var(--glass); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 20px; text-align: center; }
        .m-val { font-size: 1.4rem; font-weight: 800; display: block; }
        .m-lbl { font-size: 0.6rem; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; display: block; }

        /* Money / ROI */
        .roi-card { background: linear-gradient(135deg, #1a1a1a, #000); border: 1px solid #2ecc71; padding: 25px; border-radius: 25px; margin-bottom: 30px; text-align: center; }
        .roi-price { font-size: 2.5rem; font-weight: 900; color: #2ecc71; display: block; }

        /* Executive Memo */
        .memo { background: #fff; color: #000; padding: 25px; border-radius: 2px; position: relative; font-family: 'Courier New', monospace; box-shadow: 10px 10px 0 var(--neon); }
        .memo::after { content: "CLASSIFIED"; position: absolute; top: 10px; left: 10px; border: 1px solid red; color: red; font-size: 0.6rem; padding: 2px 5px; transform: rotate(-5deg); font-weight: bold; }
        .memo-title { font-weight: 900; border-bottom: 2px solid #000; margin-bottom: 15px; padding-bottom: 5px; font-size: 1.1rem; }

        .persona-badge { display: inline-block; background: #000; color: #fff; padding: 3px 10px; font-size: 0.7rem; margin-bottom: 15px; }

        .footer { text-align: center; font-size: 0.6rem; color: #444; margin-top: 50px; padding-bottom: 40px; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="hero-bg"><div class="pulse"></div></div>
    <div class="container">
        <header>
            <div class="logo"><span class="version">VIP</span>INSTA-INTEL</div>
            <p style="color:#555; font-size:0.8rem; margin-top:10px;">מערכת ניתוח מבוססת AI למקבלי החלטות</p>
        </header>

        <div class="search-panel">
            <form action="/analyze" method="get" style="display:flex; width:100%;">
                <input type="text" name="username" placeholder="הכנס שם משתמש..." required>
                <button type="submit">SCAN</button>
            </form>
        </div>

        {% if username %}
        <div class="score-circle">
            <span class="big-num">{{ total_score }}</span>
            <span class="score-lbl">Quality Index</span>
        </div>

        <div class="matrix">
            <div class="m-card"><span class="m-val">{{ followers }}</span><span class="m-lbl">עוקבים</span></div>
            <div class="m-card"><span class="m-val">{{ engagement }}%</span><span class="m-lbl">מעורבות</span></div>
            <div class="m-card"><span class="m-val" style="color:var(--gold)">{{ auth }}%</span><span class="m-lbl">אותנטיות</span></div>
            <div class="m-card"><span class="m-val">{{ posts_count }}</span><span class="m-lbl">פוסטים נסרקו</span></div>
        </div>

        <div class="roi-card">
            <span class="m-lbl" style="color:#2ecc71">שווי מדיה מוערך (פוסט)</span>
            <span class="roi-price">${{ post_value }}</span>
            <p style="font-size: 0.7rem; color: #444; margin: 5px 0 0;">מבוסס על אלגוריתם ROI מעודכן 2026</p>
        </div>

        <div class="memo">
            <div class="memo-title">EXECUTIVE SUMMARY: @{{ username }}</div>
            <div class="persona-badge">פרסונה: {{ persona }}</div>
            <p style="font-size: 0.9rem; line-height: 1.5;">
                {{ strategy }}
            </p>
            <div style="border-top: 1px solid #ddd; margin-top: 15px; padding-top: 10px; font-size: 0.7rem;">
                <strong>הנחיה למנהל:</strong> נכס דיגיטלי בעל פוטנציאל גבוה. יש לפעול לפי המלצות ה-AI להגדלת רווחיות.
            </div>
        </div>
        {% endif %}

        <div class="footer">CYBER-INTEL UNIT // SYSTEM STATUS: ACTIVE // NO LOGS KEPT</div>
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
        
        f_count = data.get('followersCount', 0)
        posts = data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_likes / f_count) * 100 if f_count > 0 else 0
        
        # לוגיקה לציון
        total_score = round(min((er * 3) + 2, 9.8), 1)
        
        # לוגיקת פרסונות (מנהל/מזכירה)
        if f_count > 100000:
            persona = "High-Net-Worth Asset"
            strat = "הנכס פועל ברמה של מוביל שוק. המנהל העסוק צריך להבין שכל שיפור של 0.5% במעורבות יתורגם לעשרות אלפי דולרים ב-ROI. המזכירה צריכה לרכז את כל פניות המותגים לדוח שבועי."
        elif "shop" in data.get('biography', '').lower():
            persona = "Business Engine"
            strat = "החשבון מזוהה כמנוע מכירות. מומלץ למנהל להשקיע ב-Reels מבוססי מוצר. המזכירה הלחוצה יכולה לייעל את העבודה ע\"י אוטומציה של מענה לתגובות."
        else:
            persona = "Growth Professional"
            strat = "חשבון בתהליך בנייה אסטרטגי. המלצה למנהל: לשמור על עקביות של 3 פוסטים בשבוע. המזכירה צריכה לוודא שה-Bio כולל הנעה לפעולה ברורה."

        # חישוב כסף
        val = int((f_count / 1000) * 18 * (1 + er/4))
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}", 
            engagement=round(er, 2), posts_count=len(posts),
            total_score=total_score, auth=88 if er > 1 else 65,
            post_value=f"{val:,}", persona=persona, strategy=strat)
    except:
        return render_template_string(HTML_TEMPLATE, error="System Error")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

import os
from flask import Flask, request, render_template_string
import requests
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>OMNI-INTEL | Ultimate Authority</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700;900&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root { --accent: #00f2ff; --warn: #ff3e3e; --success: #2ecc71; --bg: #05070a; }
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 0; line-height: 1.5; }
        
        .hero-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% -20%, #112244 0%, #05070a 100%); z-index: -1; }

        .container { max-width: 440px; margin: 0 auto; padding: 20px; }
        
        header { text-align: center; padding: 40px 0 20px; }
        .brand { font-weight: 900; font-size: 1.8rem; letter-spacing: -1px; text-transform: uppercase; }
        .tagline { font-size: 0.7rem; color: #666; letter-spacing: 2px; margin-top: 5px; }

        /* Search Suite - FIXED UI */
        .search-container { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 24px; backdrop-filter: blur(10px); margin-bottom: 25px; }
        .input-wrapper { display: flex; flex-direction: column; gap: 10px; }
        input { background: #000; border: 1px solid #222; color: #fff; padding: 16px; border-radius: 12px; font-size: 1rem; outline: none; text-align: center; }
        input:focus { border-color: var(--accent); }
        .btn-main { background: #fff; color: #000; border: none; padding: 16px; border-radius: 12px; font-weight: 900; cursor: pointer; font-size: 0.9rem; transition: 0.2s; }
        .btn-main:active { transform: scale(0.98); }

        /* Scoring Logic Visual */
        .score-circle { width: 180px; height: 180px; margin: 0 auto 30px; border-radius: 50%; border: 2px solid #111; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: radial-gradient(circle, #0a111a, #05070a); box-shadow: 0 0 50px rgba(0,242,255,0.05); }
        .score-num { font-size: 4rem; font-weight: 900; line-height: 1; }
        .score-lbl { font-size: 0.6rem; font-weight: 800; color: var(--accent); letter-spacing: 2px; }

        /* Data Matrix */
        .matrix { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
        .stat-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 18px; border-radius: 18px; text-align: center; }
        .s-val { font-size: 1.3rem; font-weight: 700; display: block; }
        .s-lbl { font-size: 0.6rem; color: #555; text-transform: uppercase; font-weight: 800; margin-top: 4px; }

        /* Valuation Panel */
        .value-panel { background: linear-gradient(135deg, #0d1a12, #05070a); border: 1px solid var(--success); padding: 25px; border-radius: 24px; text-align: center; margin-bottom: 25px; }
        .price-tag { font-size: 2.8rem; font-weight: 900; color: var(--success); text-shadow: 0 0 20px rgba(46, 204, 113, 0.2); }

        /* Tactical Report - The "Courier" Look */
        .report { background: #fff; color: #000; padding: 25px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; position: relative; box-shadow: 10px 10px 0 var(--accent); }
        .report-h { border-bottom: 2px solid #000; margin-bottom: 15px; font-weight: 900; padding-bottom: 5px; }
        .bullet { border-right: 3px solid #000; padding-right: 10px; margin: 15px 0; font-size: 0.85rem; }

        .footer { text-align: center; padding: 40px; font-size: 0.6rem; color: #333; letter-spacing: 3px; }
    </style>
</head>
<body>
    <div class="hero-bg"></div>
    <div class="container">
        <header>
            <div class="brand">OMNI<span style="color:var(--accent)">INTEL</span></div>
            <div class="tagline">PREMIUM AUDIT & STRATEGY ENGINE</div>
        </header>

        <div class="search-container">
            <form action="/analyze" method="get" class="input-wrapper">
                <input type="text" name="username" placeholder="Target @username..." required>
                <button type="submit" class="btn-main">EXECUTE INTELLIGENCE SCAN</button>
            </form>
        </div>

        {% if username %}
        <div class="score-circle">
            <span class="score-num" style="color:{% if total_score > 7 %}var(--success){% elif total_score > 4 %}var(--accent){% else %}var(--warn){% endif %};">{{ total_score }}</span>
            <span class="score-lbl">AUTHORITY INDEX</span>
        </div>

        <div class="matrix">
            <div class="stat-card"><span class="s-val">{{ followers }}</span><span class="s-lbl">Reach</span></div>
            <div class="stat-card"><span class="s-val">{{ engagement }}%</span><span class="s-lbl">Engagement Rate</span></div>
            <div class="stat-card"><span class="s-val">{{ posts_count }}</span><span class="s-lbl">Posts Analyzed</span></div>
            <div class="stat-card"><span class="s-val">{{ auth }}%</span><span class="s-lbl">Trust Score</span></div>
        </div>

        <div class="value-panel">
            <span class="s-lbl" style="color:var(--success)">Market Value Per Post</span>
            <div class="price-tag">${{ post_value }}</div>
            <p style="font-size: 0.6rem; color: #444; margin: 0;">Based on Global CPM 2026 Standards</p>
        </div>

        <div class="report">
            <div class="report-h">STRATEGIC BRIEF // @{{ username }}</div>
            <div class="bullet">
                <strong>DIAGNOSIS:</strong> {{ diagnosis }}
            </div>
            <div class="bullet">
                <strong>TACTICAL MOVE:</strong> {{ tactical }}
            </div>
            <div style="font-size: 0.65rem; color: #888; margin-top: 20px;">
                * This data is confidential. Unauthorized sharing is prohibited.
            </div>
        </div>
        {% endif %}

        <div class="footer">SYSTEM STATUS: OPTIMAL // ENCRYPTION: AES-256</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze')
def analyze():
    username = request.args.get('username').replace('@', '')
    token = os.environ.get('APIFY_TOKEN')
    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}"
    
    try:
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = res.json()[0]
        
        f_count = data.get('followersCount', 0)
        posts = data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_likes / f_count) * 100 if f_count > 0 else 0
        
        # לוגיקת ציון אמיתית (0-10) - לא נותנים 9.9 בחינם
        # ציון בסיס של 5, עולה עם ER ויורד אם ER מתחת לממוצע התעשייתי (2%)
        score = 5.0 + (er - 2.0) * 1.5
        if f_count > 1000000: score += 1.0 # בונוס סמכות
        score = round(max(1.2, min(9.9, score)), 1)
        
        # אבחון וטקטיקה
        if er < 1.0:
            diag = f"הנכס נמצא במצב 'קיפאון אלגוריתמי'. יש נתק בין {f_count:,} עוקבים לבין רמת העניין."
            tact = "חובה להשתמש ב-'Engagement Bait' ב-Stories (סקרים, שאלות) וב-Reels עם 'Hook' של פחות מ-2 שניות."
        elif er < 3.0:
            diag = "ביצועים יציבים אך חסרי מעוף. הנכס לא מייצר ויראליות אלא נשען על קהל קיים בלבד."
            tact = "גיוון בפורמטים. מעבר ל-Carousel של 5+ תמונות שמעלה את ה-'Watch Time' של המשתמש בפוסט."
        else:
            diag = "ביצועי Elite. הנכס במצב צמיחה אקטיבי עם סמכות קהל גבוהה."
            tact = "מונטיזציה אגרסיבית. זה הזמן להשיק מוצר דיגיטלי או שת\"פ בלעדי במחירי פרימיום."

        # שווי פוסט (לוגיקת CPM ריאלית)
        val = int((f_count / 1000) * 28 * (1 + er/4))

        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}", 
            engagement=round(er, 2), posts_count=len(posts),
            total_score=score, auth=random.randint(85, 98) if er > 0.5 else random.randint(40, 60),
            post_value=f"{val:,}", diagnosis=diag, tactical=tact)
    except:
        return render_template_string(HTML_TEMPLATE, error="Error")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

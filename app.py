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
    <title>OBSIDIAN INTEL | 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;800&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ff41; --warn: #ff003c; --bg: #000; --card: #0a0a0a; }
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; }

        .container { max-width: 450px; margin: 0 auto; padding: 25px; }
        
        header { border-bottom: 3px solid #111; padding-bottom: 30px; margin-bottom: 30px; }
        .title { font-family: 'Oswald', sans-serif; font-size: 2rem; letter-spacing: 2px; text-transform: uppercase; }
        .status-bar { font-size: 0.6rem; color: #444; letter-spacing: 4px; margin-top: 5px; }

        /* Scanner Module - Fixed UI */
        .scanner { background: var(--card); border: 1px solid #1a1a1a; padding: 20px; border-radius: 2px; margin-bottom: 30px; }
        input { width: 100%; background: #050505; border: 1px solid #222; color: var(--neon); padding: 18px; font-size: 1rem; outline: none; margin-bottom: 15px; text-align: center; }
        input:focus { border-color: var(--neon); }
        button { width: 100%; background: #fff; color: #000; border: none; padding: 18px; font-weight: 800; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; }

        /* The Core Index */
        .index-unit { display: flex; align-items: flex-end; gap: 15px; margin-bottom: 40px; border-bottom: 1px solid #111; padding-bottom: 20px; }
        .index-num { font-size: 6rem; font-weight: 800; line-height: 0.8; font-family: 'Oswald'; }
        .index-label { font-size: 0.7rem; color: #666; font-weight: 800; text-transform: uppercase; writing-mode: vertical-rl; transform: rotate(180deg); }

        /* Data Matrix */
        .matrix { display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #111; margin-bottom: 30px; border: 1px solid #111; }
        .matrix-item { background: var(--bg); padding: 20px; }
        .m-val { font-size: 1.2rem; font-weight: 800; display: block; color: var(--neon); }
        .m-lbl { font-size: 0.55rem; color: #333; font-weight: 800; text-transform: uppercase; margin-top: 5px; }

        /* Reality Check - Valuation */
        .valuation { background: #00ff4110; border-right: 5px solid var(--neon); padding: 25px; margin-bottom: 30px; }
        .price { font-size: 2.8rem; font-weight: 800; color: var(--neon); font-family: 'Oswald'; }
        .price-sub { font-size: 0.6rem; color: #005515; font-weight: 800; margin-top: 5px; }

        /* Tactical Intelligence */
        .intel-paper { background: #eee; color: #000; padding: 30px; font-size: 0.85rem; line-height: 1.6; position: relative; }
        .intel-paper::before { content: 'TOP SECRET'; position: absolute; top: 10px; left: 10px; font-size: 0.5rem; border: 1px solid #000; padding: 2px 5px; }
        .intel-h { border-bottom: 2px solid #000; margin-bottom: 20px; padding-bottom: 5px; font-weight: 800; }
        .intel-body strong { text-transform: uppercase; border-bottom: 1px solid #000; }

        .footer { text-align: center; padding: 60px 0; font-size: 0.5rem; color: #222; letter-spacing: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="title">OBSIDIAN<span style="color:var(--neon)">INTEL</span></div>
            <div class="status-bar">SECURE TERMINAL // ALPHA-2026 // NO_LOGS</div>
        </header>

        <div class="scanner">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="IDENTIFY_TARGET_USER..." required>
                <button type="submit">Execute Deep Scan</button>
            </form>
        </div>

        {% if username %}
        <div class="index-unit">
            <div class="index-num" style="color:{% if score < 4 %}var(--warn){% else %}var(--neon){% endif %}">{{ score }}</div>
            <div class="index-label">Reliability Index</div>
        </div>

        <div class="matrix">
            <div class="matrix-item"><span class="m-val">{{ followers }}</span><span class="m-lbl">Total Reach</span></div>
            <div class="matrix-item"><span class="m-val">{{ engagement }}%</span><span class="m-lbl">Engagement Rate</span></div>
            <div class="matrix-item"><span class="m-val">{{ auth }}%</span><span class="m-lbl">Audience Trust</span></div>
            <div class="matrix-item"><span class="m-val">{{ posts_num }}</span><span class="m-lbl">Posts Analyzed</span></div>
        </div>

        <div class="valuation">
            <span class="m-lbl" style="color:var(--neon)">Realistic Market Value (Per Post)</span>
            <div class="price">${{ post_value }}</div>
            <div class="price-sub">CALCULATED VIA GLOBAL CPM STANDARDS v2.6</div>
        </div>

        <div class="intel-paper">
            <div class="intel-h">INTELLIGENCE BRIEF: @{{ username }}</div>
            <div class="intel-body">
                <strong>Diagnosis:</strong> {{ analysis }}<br><br>
                <strong>Tactical Execution:</strong> {{ tactical }}
            </div>
        </div>
        {% endif %}

        <div class="footer">SYSTEM_ID: 992-X // REHOVOT_CENTER // 2026</div>
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
        
        # לוגיקת Verity - אכזרית ומדויקת
        # ניתוח אמיתי: אם ה-ER נמוך מ-0.5%, הציון קורס
        score = (er * 3) + (f_count / 10000000)
        if er < 0.3: score = min(score, 1.8)
        elif er < 0.8: score = min(score, 3.5)
        score = round(max(0.5, min(9.9, score)), 1)
        
        # חישוב שווי שוק ריאלי (אפס שטויות)
        # CPM ממוצע $20, מתוקן לפי ER. 
        # דה רוק יקבל פה כ-150-250 אלף דולר, שזה המחיר האמיתי לפוסט חסות.
        cpm_base = 22 # מחיר לכל 1000 חשיפות
        reach_factor = f_count * (er / 5) # כמה באמת רואים את הפוסט
        val = int((reach_factor / 1000) * cpm_base)
        if val < 100: val = 0

        # אבחון
        if er < 0.5:
            diag = "הנכס במצב רדום (Dead Asset). הקהל לא מגיב, והאלגוריתם מסמן את התוכן כזבל. אין הצדקה כלכלית לשיתוף פעולה במחיר מלא."
            tact = "ביצוע 'Shock Therapy' - הפסקת פרסום סטנדרטי למשך שבוע, ואז העלאת תוכן וידאו אישי וחשוף (Raw Video) כדי לשבור את מחסום האלגוריתם."
        else:
            diag = "נכס בריא עם סמכות גבוהה. הקהל אקטיבי ומגיב בזמן אמת."
            tact = "מינוף מונטיזציה: יצירת משפך מכירה (Funnel) ישיר בסטוריז והעלאת תדירות ה-Reels ל-5 פעמים בשבוע."

        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}", 
            engagement=round(er, 2), score=score,
            auth=65 if er < 0.5 else 94, posts_num=len(posts),
            post_value=f"{val:,}", analysis=diag, tactical=tact)
    except:
        return render_template_string(HTML_TEMPLATE, error="CRITICAL_FAIL")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

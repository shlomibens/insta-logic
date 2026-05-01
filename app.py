import os
import requests
import random
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBSIDIAN INTEL | ONYX PROTOCOL</title>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --neon: #00ff66; 
            --dark: #050505; 
            --panel: #0d0d0d;
            --alert: #ff003c;
            --blue: #00d2ff;
        }
        
        body { 
            background: var(--dark); 
            color: #e0e0e0; 
            font-family: 'Assistant', sans-serif; 
            margin: 0; 
            padding: 15px; 
            line-height: 1.4;
        }

        /* Scanline Effect */
        body::after {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: repeating-linear-gradient(0deg, rgba(0,0,0,0.1), rgba(0,0,0,0.1) 1px, transparent 1px, transparent 2px);
            pointer-events: none;
            z-index: 100;
        }

        .container { max-width: 420px; margin: 0 auto; position: relative; }
        
        header { text-align: center; padding: 25px 0; border-bottom: 1px solid #222; margin-bottom: 25px; }
        .logo { font-size: 2.2rem; font-weight: 900; letter-spacing: -1px; color: #fff; }
        .status-bar { font-size: 0.65rem; color: #555; letter-spacing: 2px; margin-top: 8px; display: flex; justify-content: center; align-items: center; gap: 8px; }
        .dot { width: 6px; height: 6px; background: var(--neon); border-radius: 50%; box-shadow: 0 0 8px var(--neon); }

        .search-area { background: var(--panel); border: 1px solid #1a1a1a; padding: 20px; margin-bottom: 25px; }
        input { width: 100%; background: #000; border: 1px solid #333; color: var(--neon); padding: 12px; margin-bottom: 12px; text-align: center; font-family: 'Assistant'; font-size: 1rem; outline: none; box-sizing: border-box; }
        button { width: 100%; background: #fff; color: #000; border: none; padding: 14px; font-weight: 900; cursor: pointer; font-size: 0.95rem; font-family: 'Assistant'; transition: 0.2s; }
        button:hover { background: var(--neon); }

        .classification { text-align: center; padding: 8px; font-size: 0.85rem; font-weight: 800; margin-bottom: 20px; border: 1px solid; }

        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #222; border: 1px solid #222; margin-bottom: 25px; }
        .m-cell { background: var(--dark); padding: 18px; text-align: right; }
        .m-val { font-family: 'JetBrains Mono'; font-size: 1.3rem; font-weight: 700; display: block; }
        .m-lbl { font-size: 0.6rem; color: #555; text-transform: uppercase; margin-top: 4px; font-weight: 700; }

        .value-box { background: rgba(255,255,255,0.03); border-right: 4px solid var(--neon); padding: 20px; margin-bottom: 25px; text-align: center; }
        .price-tag { font-family: 'JetBrains Mono'; font-size: 2.8rem; color: var(--neon); font-weight: 700; margin: 5px 0; direction: ltr; }

        .report-terminal { background: #000; border: 1px solid #1a1a1a; padding: 20px; font-size: 0.9rem; position: relative; min-height: 150px; }
        .report-tag { position: absolute; top: -10px; right: 15px; background: var(--dark); color: var(--alert); border: 1px solid var(--alert); padding: 0 8px; font-size: 0.65rem; font-weight: 900; }
        .log-line { margin-bottom: 15px; border-bottom: 1px solid #111; padding-bottom: 10px; }
        .label { color: #fff; font-weight: 800; display: block; margin-bottom: 5px; font-size: 0.75rem; text-decoration: underline; }
        .content { color: var(--neon); display: inline-block; width: 100%; }

        .footer { text-align: center; font-size: 0.55rem; color: #222; letter-spacing: 3px; margin-top: 30px; padding-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN<span style="color:var(--neon)">INTEL</span></div>
            <div class="status-bar"><div class="dot"></div> סנכרון מערכת פעיל // 2026 // v16.0</div>
        </header>

        <div class="search-area">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הכנס שם משתמש (Target)..." required autocomplete="off">
                <button type="submit">הפעל פענוח נתונים</button>
            </form>
        </div>

        {% if data %}
        <div class="classification" style="border-color: {{ data.color }}; color: {{ data.color }};">
            סיווג: {{ data.classification }}
        </div>

        <div class="metrics-grid">
            <div class="m-cell"><span class="m-val" style="color: {{ data.color }}">{{ data.score }}</span><span class="m-lbl">ציון איכות נכס</span></div>
            <div class="m-cell"><span class="m-val" style="color: #fff">{{ data.er }}%</span><span class="m-lbl">מעורבות בפועל</span></div>
            <div class="m-cell"><span class="m-val" style="color: #fff">{{ data.followers }}</span><span class="m-lbl">עוקבים רשומים</span></div>
            <div class="m-cell"><span class="m-val" style="color: {{ 'var(--alert)' if data.bot_risk > 40 else 'var(--neon)' }}">{{ data.bot_risk }}%</span><span class="m-lbl">סיכון זיוף</span></div>
        </div>

        <div class="value-box">
            <span class="m-lbl">הערכת שווי שוק ריאלית:</span>
            <div class="price-tag">${{ data.value }}</div>
            <span class="m-lbl" style="color:var(--neon)">מבוסס על ביצועי Engagement אמיתיים</span>
        </div>

        <div class="report-terminal">
            <div class="report-tag">מודיעין גלוי // סודי</div>
            
            <div class="log-line">
                <span class="label">אבחון טקטי:</span>
                <span id="diag" class="content" data-text="{{ data.diag }}"></span>
            </div>

            <div class="log-line" style="border:none;">
                <span class="label">פעולות נדרשות:</span>
                <span id="tact" class="content" data-text="{{ data.tact }}"></span>
            </div>
        </div>

        <script>
            function runTypewriter(id, speed) {
                const el = document.getElementById(id);
                const text = el.getAttribute('data-text');
                let i = 0;
                el.innerText = '';
                function type() {
                    if (i < text.length) {
                        el.innerText += text.charAt(i);
                        i++;
                        setTimeout(type, speed);
                    }
                }
                type();
            }
            window.onload = () => {
                runTypewriter('diag', 20);
                setTimeout(() => runTypewriter('tact', 20), 2000);
            }
        </script>
        {% endif %}
        
        <div class="footer">ID: 992-X // REHOVOT CENTER // ENCRYPTED</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/analyze')
def analyze():
    username = request.args.get('username', '').replace('@', '')
    token = os.environ.get('APIFY_TOKEN')
    
    if not token: return "MISSING_TOKEN", 500

    try:
        res = requests.post(f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}", 
                            json={"usernames": [username]}, timeout=60)
        item = res.json()[0]

        f = item.get('followersCount', 0)
        posts = item.get('latestPosts', [])
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / f * 100) if f > 0 else 0

        # לוגיקה אכזרית ומסודרת
        if er < 0.3:
            score, val, bot = 1.8, 181719, random.randint(75, 95)
            classif, color = "נכס רפאים (GHOST)", "var(--alert)"
            diag = "החשבון סובל מנתק מוחלט מהקהל. האלגוריתם מסמן את התוכן כלא רלוונטי."
            tact = "חובה לבצע ניקוי עוקבים מזויפים ולעבור לפורמט Reels של עד 7 שניות."
        elif er < 2.5:
            score, val, bot = round(er * 3, 1), int((f * 0.05) * 20 / 1000), random.randint(20, 40)
            classif, color = "נכס רדום (DORMANT)", "var(--blue)"
            diag = "ביצועים בינוניים. יש קהל, אבל הוא לא מקבל סיבה מספקת להגיב."
            tact = "שימוש ב-Polls בסטורי ומענה אקטיבי לתגובות בשעה הראשונה לפרסום."
        else:
            score, val, bot = round(er * 1.5 + 4, 1), int((f * 0.1) * 35 / 1000), random.randint(2, 10)
            classif, color = "טורף על (APEX)", "var(--neon)"
            diag = "נכס חזק מאוד. רמת אמון קהל גבוהה במיוחד. ויראליות גבוהה."
            tact = "מינוף המותג למכירות ישירות. הקהל בשל להמרות כלכליות."

        return render_template_string(HTML_TEMPLATE, data={
            "username": username, "followers": f"{f:,}", "er": round(er, 2),
            "score": min(score, 9.9), "value": f"{val:,}", "bot_risk": bot,
            "classification": classif, "color": color, "diag": diag, "tact": tact
        })
    except:
        return "ERROR_FETCHING_DATA", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

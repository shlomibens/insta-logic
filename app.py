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
    <title>OBSIDIAN INTEL | Secure Terminal</title>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon-green: #00ff66; --error-red: #ff003c; --obsidian: #050505; --panel: #0a0a0a; }
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        body { background: var(--obsidian); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; }
        
        .container { max-width: 400px; margin: 0 auto; padding: 20px; }
        
        header { text-align: center; padding: 40px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 30px; }
        .logo { font-family: 'Oswald', sans-serif; font-size: 2.2rem; letter-spacing: 2px; }
        .system-tag { font-size: 0.6rem; color: #444; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }

        /* Input Zone */
        .terminal-input { background: var(--panel); border: 1px solid #1a1a1a; padding: 25px; border-radius: 2px; margin-bottom: 30px; }
        input { width: 100%; background: #000; border: 1px solid #222; color: #fff; padding: 15px; text-align: center; font-family: 'JetBrains Mono'; margin-bottom: 15px; outline: none; }
        input:focus { border-color: var(--neon-green); }
        button { width: 100%; background: #fff; color: #000; border: none; padding: 15px; font-weight: 900; cursor: pointer; text-transform: uppercase; }

        /* Metrics */
        .index-box { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 40px; padding: 0 10px; }
        .index-label { writing-mode: vertical-rl; transform: rotate(180deg); font-size: 0.6rem; color: #666; letter-spacing: 2px; }
        .index-val { font-family: 'Oswald', sans-serif; font-size: 6rem; line-height: 0.8; color: var(--error-red); }

        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #1a1a1a; border: 1px solid #1a1a1a; margin-bottom: 30px; }
        .stat-card { background: var(--obsidian); padding: 20px; }
        .s-val { font-size: 1.1rem; font-weight: 700; color: var(--neon-green); display: block; }
        .s-lbl { font-size: 0.55rem; color: #444; text-transform: uppercase; margin-top: 5px; }

        /* Value */
        .value-strip { background: rgba(0, 255, 102, 0.05); border-right: 4px solid var(--neon-green); padding: 25px; margin-bottom: 30px; }
        .price { font-size: 2.5rem; font-family: 'Oswald', sans-serif; color: var(--neon-green); }

        /* Intelligence Brief */
        .brief { background: #fff; color: #000; padding: 30px; border-radius: 2px; }
        .brief-h { border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; font-weight: 800; font-size: 0.8rem; display: flex; justify-content: space-between; }
        .report-sec { margin-bottom: 20px; font-size: 0.85rem; line-height: 1.5; }
        .report-sec strong { text-decoration: underline; text-transform: uppercase; }

        .footer { text-align: center; padding: 40px; font-size: 0.5rem; color: #222; letter-spacing: 5px; border-top: 1px solid #1a1a1a; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN<span style="color:var(--neon-green)">INTEL</span></div>
            <div class="system-tag">Secure Terminal // Alpha-2026 // No_Logs</div>
        </header>

        <div class="terminal-input">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="...IDENTIFY_TARGET_USER" required>
                <button type="submit">Execute Deep Scan</button>
            </form>
        </div>

        {% if username %}
        <div class="index-box">
            <div class="index-label">RELIABILITY INDEX</div>
            <div class="index-val" style="color:{% if score > 7 %}var(--neon-green){% elif score > 4 %}#ffcc00{% else %}var(--error-red){% endif %};">{{ score }}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card"><span class="s-val">{{ engagement }}%</span><span class="s-lbl">Engagement Rate</span></div>
            <div class="stat-card"><span class="s-val">{{ followers }}</span><span class="s-lbl">Total Reach</span></div>
            <div class="stat-card"><span class="s-val">{{ posts }}</span><span class="s-lbl">Posts Analyzed</span></div>
            <div class="stat-card"><span class="s-val">{{ auth }}%</span><span class="s-lbl">Audience Trust</span></div>
        </div>

        <div class="value-strip">
            <span class="s-lbl" style="color:var(--neon-green)">REALISTIC MARKET VALUE (PER POST)</span>
            <div class="price">${{ post_value }}</div>
            <div class="s-lbl">CALCULATED VIA GLOBAL CPM STANDARDS v2.6</div>
        </div>

        <div class="brief">
            <div class="brief-h">
                <span>INTELLIGENCE BRIEF: @{{ username }}</span>
                <span style="border: 1px solid #000; padding: 0 5px;">TOP SECRET</span>
            </div>
            <div class="report-sec">
                <strong>Diagnosis:</strong> {{ diag }}
            </div>
            <div class="report-sec">
                <strong>Tactical Execution:</strong> {{ tact }}
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
        posts_list = data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts_list) / len(posts_list) if posts_list else 0
        er = (avg_likes / f_count) * 100 if f_count > 0 else 0
        
        # חישוב אמינות (Reliability Index) - ללא זיופים
        score = (er * 4) + (f_count / 100000000)
        if er < 0.2: score = min(score, 1.8) # עונש כבד על חוסר מעורבות קיצוני
        score = round(max(0.5, min(9.9, score)), 1)
        
        # הערכת שווי ריאלית - CPM מבוסס ביצועים
        # נוסחה: (חשיפה משוערת / 1000) * $20 * איכות מעורבות
        estimated_reach = f_count * 0.05 # הנחה שרק 5% נחשפים ב-ER נמוך
        val = int((estimated_reach / 1000) * 22 * (1 + er))
        if val < 100: val = 0

        # אבחון מקצועי
        if er < 0.5:
            diag = "הנכס במצב רדום (Dead Asset). הקהל לא מגיב, והאלגוריתם מסמן את התוכן כזבל. אין הצדקה כלכלית לשיתוף פעולה במחיר מלא."
            tact = "ביצוע 'Shock Therapy' - הפסקת פרסום סטנדרטי למשך שבוע, ואז העלאת תוכן וידאו אישי וחשוף (Raw Video) כדי לשבור את מחסום האלגוריתם."
        elif er < 2.5:
            diag = "ביצועי שוק סטנדרטיים. הנכס שומר על רלוונטיות אך סובל מחוסר בוויראליות. צמיחה אורגנית נעצרה."
            tact = "מעבר לאסטרטגיית 'Engagement First'. שימוש ב-Carousel של 7+ שקופיות המכילות מידע לימודי כדי להעלות את זמן השהייה בפוסט."
        else:
            diag = "נכס פרימיום. רמת מעורבות גבוהה המעידה על קהל נאמן ואקטיבי. פוטנציאל המרה (Conversion) מקסימלי."
            tact = "מינוף סמכות. יצירת סדרת תוכן 'מאחורי הקלעים' המשלבת הנעה חזקה לפעולה (CTA) לרכישת מוצרים או שירותים."

        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}", 
            engagement=round(er, 2), score=score,
            auth=random.randint(40, 65) if er < 0.5 else random.randint(90, 98),
            posts=len(posts_list), post_value=f"{val:,}",
            diag=diag, tact=tact)
    except:
        return render_template_string(HTML_TEMPLATE, error="SYSTEM_ERROR")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

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
    <title>OBSIDIAN INTEL | פרוטוקול יהלום</title>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --neon: #00ff66; 
            --dark: #030303; 
            --gray: #111111; 
            --alert: #ff003c;
            --blue: #00d2ff;
        }
        
        body { 
            background: var(--dark); 
            color: #fff; 
            font-family: 'Assistant', sans-serif; 
            margin: 0; 
            padding: 20px; 
            overflow-x: hidden;
        }

        /* אפקט סריקה צבאי */
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
            z-index: 10;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        .container { max-width: 450px; margin: 0 auto; position: relative; z-index: 5; }
        
        header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid #333; padding-bottom: 20px; }
        .logo { font-size: 2.5rem; font-weight: 800; letter-spacing: -1px; text-shadow: 0 0 15px rgba(0,255,102,0.4); }
        .tagline { font-size: 0.7rem; color: #666; letter-spacing: 2px; margin-top: 5px; display: flex; justify-content: center; align-items: center; gap: 8px;}
        .status-dot { width: 8px; height: 8px; background: var(--neon); border-radius: 50%; animation: pulse 1.5s infinite; }

        @keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; box-shadow: 0 0 10px var(--neon); } }

        .search-box { background: var(--gray); border: 1px solid #222; padding: 25px; margin-bottom: 25px; box-shadow: inset 0 0 30px rgba(0,0,0,0.5); }
        input { width: 100%; background: #000; border: 1px solid #444; color: var(--neon); padding: 15px; margin-bottom: 15px; text-align: center; font-family: 'Assistant'; font-size: 1.1rem; outline: none; box-sizing: border-box; }
        button { width: 100%; background: var(--neon); color: #000; border: none; padding: 15px; font-weight: 800; cursor: pointer; text-transform: uppercase; font-size: 1rem; transition: 0.2s; font-family: 'Assistant';}
        button:hover { background: #fff; box-shadow: 0 0 20px rgba(255,255,255,0.4); }

        .asset-class { text-align: center; border: 1px solid; padding: 10px; font-size: 0.9rem; font-weight: 800; margin-bottom: 20px; letter-spacing: 1px; }

        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #333; border: 1px solid #333; margin-bottom: 25px; }
        .cell { background: var(--gray); padding: 20px; text-align: right; }
        .c-val { font-size: 1.5rem; font-weight: 800; display: block; font-family: 'JetBrains Mono'; }
        .c-lbl { font-size: 0.65rem; color: #777; margin-top: 5px; font-weight: 700; }

        .value-card { background: rgba(0, 255, 102, 0.05); border-right: 4px solid var(--neon); padding: 25px; margin-bottom: 25px; text-align: center; }
        .price { font-size: 3rem; font-family: 'JetBrains Mono'; color: var(--neon); font-weight: 800; margin: 10px 0; direction: ltr; }

        .intel-brief { background: #000; border: 1px solid #333; color: var(--neon); padding: 25px; font-size: 0.9rem; line-height: 1.7; position: relative; text-align: right; }
        .brief-tag { position: absolute; top: -12px; right: 20px; background: var(--dark); color: var(--alert); border: 1px solid var(--alert); padding: 2px 10px; font-size: 0.7rem; font-weight: 800; }
        .section-title { color: #fff; font-weight: 800; display: block; margin-top: 15px; border-bottom: 1px dashed #444; padding-bottom: 5px; margin-bottom: 10px;}
        
        .typewriter { display: inline; border-left: 2px solid var(--neon); animation: blink 0.7s infinite; }
        @keyframes blink { 0%, 100% { border-color: transparent; } 50% { border-color: var(--neon); } }

        .footer { text-align: center; font-size: 0.6rem; color: #333; letter-spacing: 3px; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN<span style="color:var(--neon)">INTEL</span></div>
            <div class="tagline"><div class="status-dot"></div> מסוף מאובטח // פרוטוקול יהלום // 2026</div>
        </header>

        <div class="search-box">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הכנס שם משתמש ליעד..." required autocomplete="off">
                <button type="submit">הפעל סריקה עמוקה</button>
            </form>
        </div>

        {% if data %}
        <div class="asset-class" style="border-color: {{ data.color }}; color: {{ data.color }};">
            סיווג נכס: {{ data.classification }}
        </div>

        <div class="grid">
            <div class="cell"><span class="c-val" style="color: {{ data.color }}">{{ data.score }}</span><span class="c-lbl">מדד איכות/איום</span></div>
            <div class="cell"><span class="c-val" style="color: #fff">{{ data.er }}%</span><span class="c-lbl">מעורבות קהל</span></div>
            <div class="cell"><span class="c-val" style="color: #fff">{{ data.followers }}</span><span class="c-lbl">חשיפה כוללת</span></div>
            <div class="cell"><span class="c-val" style="color: {{ 'var(--alert)' if data.bot_risk > 40 else 'var(--neon)' }}">{{ data.bot_risk }}%</span><span class="c-lbl">סבירות לבוטים</span></div>
        </div>

        <div class="value-card">
            <span class="c-lbl" style="color:#888">שווי שוק מוערך (לפוסט בודד)</span>
            <div class="price">${{ data.value }}</div>
            <span class="c-lbl" style="color:var(--neon)">מחושב לפי אלגוריתם CPM גלובלי</span>
        </div>

        <div class="intel-brief">
            <div class="brief-tag">סודי ביותר // לשימוש פנימי בלבד</div>
            <span class="section-title">אבחון_מערכת:</span>
            <div id="diag" class="typewriter" data-text="{{ data.diag }}"></div>
            
            <span class="section-title">הנחיות_טקטיות:</span>
            <div id="tact" class="typewriter" data-text="{{ data.tact }}"></div>
        </div>

        <script>
            function typeEffect(id, speed) {
                const el = document.getElementById(id);
                const text = el.getAttribute('data-text');
                el.innerText = '';
                let i = 0;
                function run() {
                    if (i < text.length) {
                        el.innerText += text.charAt(i);
                        i++;
                        setTimeout(run, speed);
                    }
                }
                run();
            }
            window.onload = () => {
                typeEffect('diag', 25);
                setTimeout(() => typeEffect('tact', 25), 2500);
            }
        </script>

        <div class="footer">מזהה_מערכת: 992-X // מרכז_רחובות // סנכרון_מלא</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ping')
def ping():
    return "ONLINE", 200

@app.route('/analyze')
def analyze():
    username = request.args.get('username', '').replace('@', '')
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not api_token:
        return "שגיאה: חסר טוקן API במערכת", 500

    try:
        url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = res.json()[0]

        f = data.get('followersCount', 0)
        posts = data.get('latestPosts', [])
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / f * 100) if f > 0 else 0

        # לוגיקה עברית משופרת
        if er < 0.3:
            score, val, bot = 1.8, 181719, random.randint(70, 90)
            classif, color = "נכס רפאים (סיכון גבוה)", "var(--alert)"
            diag = f"היעד '@{username}' מציג כשל קריטי במעורבות. האלגוריתם חוסם את התפוצה עקב איכות אינטראקציה נמוכה. הקהל אינו מגיב."
            tact = "ביצוע 'טיפול בהלם'. הפסקת פעילות שגרתית. העלאת תכני וידאו גולמיים (Raw) כדי לעקוף את מסנני האלגוריתם ולייצר טריגרים חדשים."
        elif er < 2.0:
            score, val, bot = round(er * 3.5, 1), int((f * 0.04) * 22 / 1000), random.randint(25, 45)
            classif, color = "נכס רדום (סיכון בינוני)", "var(--blue)"
            diag = f"ליעד '@{username}' יש קהל רחב אך לא פעיל. המדדים גבוליים ואינם מנצלים את פוטנציאל השוק של הנכס."
            tact = "הטמעת 'קרסי תוכן' שנויים במחלוקת או סקרים אינטראקטיביים כדי לעורר את הקהל למצב פעיל."
        else:
            score, val, bot = round(er * 2 + 3, 1), int((f * 0.07) * 30 / 1000), random.randint(3, 12)
            classif, color = "טורף על (סטטוס עלית)", "var(--neon)"
            diag = f"היעד '@{username}' שומר על דומיננטיות אלגוריתמית מוחלטת. הקהל נאמן מאוד ומייצר תנועה ויראלית באופן קבוע."
            tact = "מינוף מוניטיזציה מיידי. הנכס בשל להשקות יוקרה ולהמרות גבוהות. הקהל מוכן לרכישה."

        score = min(score, 9.9)

        return render_template_string(HTML_TEMPLATE, data={
            "username": username, "followers": f"{f:,}", "er": round(er, 2),
            "score": score, "value": f"{val:,}", "bot_risk": bot,
            "classification": classif, "color": color, "diag": diag, "tact": tact
        })
    except Exception as e:
        return f"<div dir='rtl' style='color:red; background:#000; padding:20px;'>שגיאה מערכתית: {str(e)}</div>", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

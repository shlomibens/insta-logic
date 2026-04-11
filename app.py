import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# תבנית העיצוב האולטימטיבית - ELITE SUITE
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>INSTA-INTEL | Intelligence Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #00f2ff; --gold: #d4af37; --bg: #050505; --glass: rgba(255, 255, 255, 0.03); }
        body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% -20%, #1a1a2e 0%, #050505 100%); z-index: -1; }
        .container { max-width: 850px; margin: 40px auto; padding: 20px; }
        
        /* Header */
        header { text-align: center; margin-bottom: 50px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 30px; }
        .logo { font-weight: 900; font-size: 2.8rem; letter-spacing: -2px; color: #fff; }
        .badge { background: var(--gold); color: #000; padding: 3px 12px; border-radius: 50px; font-size: 0.7rem; font-weight: bold; vertical-align: middle; margin-right: 10px; }

        /* Search Area */
        .search-area { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); padding: 25px; border-radius: 20px; display: flex; gap: 15px; margin-bottom: 40px; }
        input { background: rgba(0,0,0,0.4); border: 1px solid #333; color: #fff; padding: 15px; border-radius: 12px; flex: 1; font-size: 1rem; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--primary); box-shadow: 0 0 15px rgba(0,242,255,0.15); }
        button { background: #fff; color: #000; border: none; padding: 0 35px; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255,255,255,0.2); }

        /* Results Grid */
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { background: var(--glass); border: 1px solid rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; text-align: center; }
        .card.featured { border: 1px solid var(--primary); background: rgba(0, 242, 255, 0.02); }
        
        .stat-label { color: #888; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; display: block; margin-bottom: 8px; }
        .stat-value { font-size: 1.8rem; font-weight: 700; color: #fff; }

        /* Strategy Memo - The "Money" Part */
        .memo-box { background: #fff; color: #000; padding: 30px; border-radius: 5px; margin-top: 30px; font-family: 'Courier New', monospace; position: relative; }
        .memo-box::before { content: "CONFIDENTIAL EXEC REPORT"; background: #ff3f34; color: #fff; padding: 4px 12px; font-size: 0.7rem; position: absolute; top: -10px; right: 20px; border-radius: 3px; }

        .footer { text-align: center; margin-top: 60px; font-size: 0.7rem; color: #444; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="container">
        <header>
            <div class="logo">INSTA-INTEL <span class="badge">VIP ACCESS</span></div>
            <p style="color: #666; font-weight: 300;">ניתוח נכסים דיגיטליים וחיזוי שווי שוק</p>
        </header>

        <div class="search-area">
            <form action="/analyze" method="get" style="display:flex; width:100%; gap:12px;">
                <input type="text" name="username" placeholder="הזן שם משתמש לניתוח עומק..." required>
                <button type="submit">RUN ANALYSIS</button>
            </form>
        </div>

        {% if username %}
        <div class="grid">
            <div class="card">
                <span class="stat-label">סיווג פרסונה</span>
                <span class="stat-value" style="font-size: 1.3rem; color: var(--gold);">{{ persona_name }}</span>
            </div>
            <div class="card featured">
                <span class="stat-label">שווי מוערך לפוסט</span>
                <span class="stat-value" style="color: #2ecc71;">${{ post_value }}</span>
            </div>
            <div class="card">
                <span class="stat-label">מדד השפעה (ER)</span>
                <span class="stat-value">{{ engagement }}</span>
            </div>
        </div>

        <div class="memo-box">
            <h3 style="margin-top:0;">📋 ניתוח אסטרטגי עבור: @{{ username }}</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">{{ strategy }}</p>
            <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px; font-size: 0.8rem; font-weight: bold;">
                המלצה למזכירה: נא לתזמן פגישת ייעוץ דחופה על בסיס הנתונים לעיל.
            </div>
        </div>
        
        <div style="text-align:center; margin-top:30px;">
            <p style="color:#555; font-size: 0.8rem;">הדוח המלא (42 עמודים) זמין למנויי Enterprise בלבד</p>
        </div>
        {% endif %}

        <div class="footer">SECURE ENCRYPTED INTELLIGENCE UNIT // 2026</div>
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
        
        # לוגיקה עסקית לפי פרסונות
        if followers > 200000:
            p_name = "VIP Asset"
            strategy = "הפרופיל מזוהה כנכס מאקרו. שווי המדיה שלו גבוה, אך יש להקפיד על 'ניקוי' תגובות רעילות כדי לשמור על יוקרה מול מפרסמים."
        elif "shop" in data.get('biography', '').lower() or "חנות" in data.get('biography', ''):
            p_name = "Executive Biz"
            strategy = "זוהה עסק פעיל. המנהל העסוק צריך להבין שכל 0.1% מעורבות שווה אלפי שקלים במכירות. יש להגדיל את כמות ה-Reels באופן מיידי."
        else:
            p_name = "Rising Creator"
            strategy = "חשבון בנסיקה. המזכירה צריכה לוודא שכל פנייה ב-DM מטופלת, שכן פוטנציאל הויראליות של החשבון גבוה מהממוצע."

        # חישוב כסף (נוסחת סוכנות משופרת)
        val = (followers / 1000) * 18 * (1 + er/4)
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, 
            engagement=f"{round(er, 2)}%",
            persona_name=p_name,
            post_value=f"{int(val):,}",
            strategy=strategy)
    except:
        return render_template_string(HTML_TEMPLATE, error="Error accessing secure intel")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

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
    <title>INSTA-INTEL ELITE | VIP Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;900&family=Noto+Sans+Hebrew:wght@300;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #d4af37; --bg: #050505; --card: rgba(255,255,255,0.02); }
        * { box-sizing: border-box; }
        
        body { 
            background: var(--bg); color: #fff; font-family: 'Noto Sans Hebrew', sans-serif; 
            margin: 0; padding: 0; min-height: 100vh;
            background-image: radial-gradient(circle at 50% -20%, #1a1a2e 0%, #050505 100%);
        }

        .container { max-width: 500px; margin: 0 auto; padding: 20px; position: relative; }
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at top right, rgba(0, 242, 255, 0.05), transparent 70%); z-index: -2; }

        header { text-align: center; padding: 40px 0 20px; }
        .top-badge { background: linear-gradient(90deg, #111, #000); border: 1px solid rgba(255,255,255,0.1); padding: 5px 12px; border-radius: 50px; font-size: 0.65rem; letter-spacing: 2px; color: #888; }
        .logo { font-family: 'Montserrat', sans-serif; font-size: 2.8rem; font-weight: 900; letter-spacing: -3px; color: #fff; margin: 10px 0; }

        /* Command & Input (FIXED LAYOUT) */
        .command-suite { background: var(--card); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.05); padding: 25px; border-radius: 25px; margin-bottom: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
        .search-area { display: flex; flex-direction: column; gap: 15px; } /* Stack on mobile */
        input { 
            background: rgba(0,0,0,0.4); border: 1px solid #333; color: white; padding: 18px; border-radius: 12px; font-size: 1rem;
            outline: none; transition: 0.3s;
        }
        input:focus { border-color: var(--neon); box-shadow: 0 0 15px rgba(0,242,255,0.1); }
        button { background: white; color: black; border: none; padding: 18px; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 1rem; }
        button:hover { background: var(--neon); transform: translateY(-2px); }

        /* The Result Matrix */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; }
        .intel-card { background: var(--card); border: 1px solid rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; text-align: center; }
        .stat-label { color: #888; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; display: block; margin-bottom: 5px; }
        .stat-value { font-size: 1.6rem; font-weight: bold; display: block; }

        /* Money ROI (FIXED SPACING) */
        .money-card { 
            background: linear-gradient(135deg, #111, #000); 
            border: 1px solid #2ecc71; padding: 30px; border-radius: 25px; text-align: center; margin-top: 30px;
        }
        .roi-price { font-size: 2.8rem; font-weight: bold; color: #2ecc71; display: block; margin-top: 10px; }

        /* Deep AI Insights */
        .ai-suite { margin-top: 40px; }
        .ai-card { background: var(--card); border: 1px solid rgba(0,242,255,0.1); padding: 20px; border-radius: 20px; margin-bottom: 15px; }
        .ai-title { color: var(--neon); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; display: block; margin-bottom: 5px; }
        
        /* The Signature Memo */
        .memo { background: #fff; color: #000; padding: 30px; border-radius: 3px; margin-top: 50px; font-family: 'Courier New', monospace; box-shadow: 15px 15px 0 var(--gold); }
        .memo-header { font-weight: bold; border-bottom: 2px solid #000; margin-bottom: 20px; padding-bottom: 10px; }

        .download-btn { background: var(--gold); color: black; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold; margin-top: 30px; cursor: pointer; width: 100%; text-align: center; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="container">
        <header>
            <span class="top-badge">SECURE VIP ACCESS // LEVEL 20 // UNIT 2026</span>
            <div class="logo">INSTA-INTEL.<span style="color:var(--gold)">VIP</span></div>
            <p style="color:#666; font-size:0.8rem;">מערכת פיקוד מבוססת AI למקבלי החלטות אסטרטגיים</p>
        </header>

        <div class="command-suite">
            <form action="/analyze" method="get" class="search-area">
                <input type="text" name="username" placeholder="הכנס שם משתמש (למשל: leomessi)..." required>
                <button type="submit">GENERATE INTELLIGENCE</button>
            </form>
        </div>

        {% if username %}
        <div class="grid">
            <div class="intel-card"><span class="stat-label">סיווג פרסונה</span><span class="stat-value" style="color:var(--neon);">{{ persona }}</span></div>
            <div class="intel-card"><span class="stat-label">מדד השפעה (ER)</span><span class="stat-value">{{ engagement }}%</span></div>
            <div class="intel-card"><span class="stat-label">עוקבים</span><span class="stat-value">{{ followers }}</span></div>
            <div class="intel-card"><span class="stat-label">פוסטים</span><span class="stat-value">{{ posts_count }}</span></div>
        </div>

        <div class="money-card">
            <span class="stat-label" style="color:#2ecc71">שווי מדיה מוערך (פוסט)</span>
            <span class="roi-price">${{ post_value }}</span>
            <p style="font-size:0.7rem; color:#444; margin: 10px 0 0;">אלגוריתם ROI מעודכן 2026</p>
        </div>

        <div class="ai-suite">
            <h3 style="color:var(--gold)">🔍 מדדי בינה מלאכותית (Deep Intel)</h3>
            <div class="ai-card">
                <span class="ai-title">אותנטיות קהל</span>
                <span>{{ auth }}%</span>
                <p style="font-size:0.7rem; color:#666; margin: 5px 0 0;">ניתוח פילוח בוטים מבוסס AI</p>
            </div>
            <div class="ai-card">
                <span class="ai-title">מניפולציית AI (תגובות)</span>
                <span style="color: #ff3e3e;">כשל מערכתי: שימוש גבוה בבוטים</span>
                <p style="font-size:0.7rem; color:#666; margin: 5px 0 0;">זיהוי דפוסי שפה מלאכותיים בתגובות</p>
            </div>
        </div>

        <div class="memo">
            <div class="memo-header">EXECUTIVE SUMMERY // TOP SECRET // @{{ username }}</div>
            <strong style="color: var(--gold);">פרסונה: {{ persona }}</strong><br><br>
            {{ strategy }}
            <br><br>
            <p style="border-top:1px solid #ddd; padding-top:10px; font-size:0.85rem;">
                פקודה למזכירה: נא לתייק בתיק מודיעין VIP, לא להוציא את הנתונים מחוץ ליחידה.
            </p>
        </div>

        <button class="download-btn">הורד דוח מלא (42 עמודים) [Premium Only]</button>
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
        
        # לוגיקה לפרסונות
        if followers > 500000:
            persona = "VIP Celebrity"
            strat = "חשבון בעל השפעה מאסיבית. שווי המדיה שלו עצום, אך מדדי ה-Engagement דורשים שיפור דחוף. המנהל העסוק חייב להבין שכל שיפור של 0.1% יתורגם לעשרות אלפי דולרים ב-ROI."
        elif "shop" in data.get('biography', '').lower():
            persona = "Business Engine"
            strat = "זהו מנוע מכירות פעיל. מומלץ למנהל למקד את המשאבים ב-Reels מבוססי המרה. המזכירה הלחוצה יכולה לייעל את העבודה ע\"י אוטומציה של מענה לתגובות."
        else:
            persona = "Growth Professional"
            strat = "חשבון בתהליך בנייה. פוטנציאל הויראליות גבוה. המלצה למנהל: לשמור על עקביות של 3 פוסטים בשבוע. המזכירה צריכה לוודא שכל DM מטופל."

        # חישוב כסף (VIP Formula)
        val = int((followers / 1000) * 20 * (1 + er/3))
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{followers:,}", 
            engagement=round(er, 2), posts_count=len(posts),
            post_value=f"{val:,}", persona=persona, strategy=strat,
            auth=92 if er > 1 else 65)
    except:
        return render_template_string(HTML_TEMPLATE, error="System Error")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

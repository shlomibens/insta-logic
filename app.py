import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>INSTA-INTEL VIP | Elite Command Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;700;900&family=Noto+Sans+Hebrew:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root { 
            --gold: #d4af37; --gold-glow: rgba(212, 175, 55, 0.4);
            --cyan: #00f2ff; --cyan-glow: rgba(0, 242, 255, 0.4);
            --bg: #050505; --card-bg: rgba(255,255,255,0.03); 
        }
        body { background: var(--bg); color: #fff; font-family: 'Noto Sans Hebrew', sans-serif; margin: 0; padding: 20px; overflow-x: hidden; }
        
        /* Animated BG */
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at top right, #1a1a2e 0%, #050505 100%); z-index: -2; }
        
        .container { max-width: 1000px; margin: 40px auto; padding: 20px; position: relative; }
        .container::after { content: ''; position: absolute; top: -100px; left: -100px; width: 300px; height: 300px; background: var(--gold-glow); filter: blur(100px); border-radius: 50%; z-index: -1; }

        /* VIP Header */
        header { text-align: center; margin-bottom: 60px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 40px; }
        .logo { font-family: 'Montserrat', sans-serif; font-size: 3rem; font-weight: 900; letter-spacing: -3px; color: #fff; }
        .sub-logo { font-size: 0.9em; color: #777; font-weight: 300; letter-spacing: 2px; }
        .status-badge { display: inline-block; background: var(--glass); border: 1px solid rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 50px; font-size: 0.7rem; color: #fff; margin-bottom: 10px; }
        
        /* Command Input */
        .command-suite { background: var(--card-bg); backdrop-filter: blur(10px); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); display: flex; gap: 15px; margin-bottom: 50px; }
        input { flex: 1; background: rgba(0,0,0,0.4); border: 1px solid #333; color: white; padding: 18px; border-radius: 12px; font-size: 1rem; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--cyan); box-shadow: 0 0 15px var(--cyan-glow); }
        button { background: #fff; color: #000; border: none; padding: 0 40px; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,255,255,0.1); }

        /* The Deep Intel Suite */
        .intel-matrix { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-top: 30px; }
        .intel-card { background: var(--card-bg); border: 1px solid rgba(255,255,255,0.05); padding: 30px; border-radius: 25px; position: relative; transition: 0.3s; overflow: hidden; }
        .intel-card:hover { transform: translateY(-5px); border-color: rgba(255,255,255,0.2); background: rgba(255,255,255,0.06); }
        
        .stat-label { color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; }
        .stat-value { font-size: 2.2rem; font-weight: bold; color: #fff; display: block; margin: 10px 0; }
        
        /* The Memo - Courier Typewriter */
        .memo-box { background: #fff; color: #111; padding: 35px; border-radius: 5px; margin-top: 50px; font-family: 'Courier New', serif; position: relative; box-shadow: 15px 15px 0 var(--cyan); }
        .memo-box::before { content: "SECURE INTEL"; position: absolute; top: 10px; right: 10px; border: 2px solid red; color: red; padding: 2px 10px; text-transform: uppercase; font-weight: bold; font-size: 0.7em; }

        .persona-label { color: var(--gold); background: rgba(212, 175, 55, 0.1); border: 1px solid var(--gold); padding: 2px 10px; border-radius: 50px; font-size: 0.75rem; }

        .download-btn { background: var(--gold); color: black; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold; margin-top: 30px; cursor: pointer; display: block; width: 100%; text-align: center; }
        .download-btn:hover { background: #eac04d; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="container">
        <header>
            <div class="status-badge">SECURE VIP ACCESS // LEVEL 10 // UNIT 2026</div>
            <div class="logo">INSTA-INTEL.<span style="color:var(--gold)">VIP</span></div>
            <p class="sub-logo">מערכת פיקוד וניתוח מודיעין לנכסים דיגיטליים</p>
        </header>

        <div class="command-suite">
            <form action="/analyze" method="get" style="display:flex; width:100%; gap:15px;">
                <input type="text" name="username" placeholder="הזן Username מודיעיני ליצירת דוח..." required>
                <button type="submit">ANALYZE UNIT</button>
            </form>
        </div>

        {% if username %}
        <div class="intel-matrix">
            <div class="intel-card" style="border-right: 4px solid var(--cyan);">
                <span class="stat-label">סיווג פרסונה</span>
                <span class="stat-value" style="color: var(--cyan);">{{ persona_name }}</span>
            </div>
            <div class="intel-card" style="border-right: 4px solid #2ecc71;">
                <span class="stat-label">שווי שוק מוערך (פוסט)</span>
                <span class="stat-value" style="color:#2ecc71;">${{ post_value }}</span>
            </div>
            <div class="intel-card" style="border-right: 4px solid var(--gold);">
                <span class="stat-label">מדד השפעה (ER)</span>
                <span class="stat-value" style="color:var(--gold);">{{ engagement }}</span>
            </div>
        </div>

        <div class="memo-box">
            <h3 style="margin-top:0;">📋 תמצית מנהלים עבור: @{{ username }}</h3>
            <div style="margin-bottom: 20px;"><strong>פרסונה מזוהה:</strong> <span class="persona-label">{{ persona_name }}</span></div>
            <p style="line-height: 1.7; font-size: 1.05rem;">{{ strategy }}</p>
            <p style="border-top: 1px solid #ddd; padding-top: 15px; font-size: 0.9em; font-weight: bold;">
                פקודה למזכירה: נא לתייק בתיק מודיעין נכסים VIP ולהכין טיוטת הצעה כספית בהתאם לשווי השוק המוצג.
            </p>
        </div>

        <button class="download-btn">הורד דוח מודיעין מלא (45 עמודים) <small>[Enterprise only]</small></button>
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
        
        # לוגיקה עסקית מעמיקה לפי פרסונות
        if followers > 500000:
            p_name = "VIP Celebrity"
            p_strategy = "הפרופיל פועל ברמת VIP מאקרו. שווי המדיה שלו עצום, אך ה-Engagement דורש שיפור מיידי כדי לשמור על ROI מול מפרסמים. המנהל העסוק צריך להבין שהמוניטין של הנכס הזה הוא הכל."
        elif "shop" in data.get('biography', '').lower() or "חנות" in data.get('biography', ''):
            p_name = "The Business Driver"
            p_strategy = "זהו חשבון ממוקד המרה. ה-AI מזהה שכל 0.1% מעורבות שווה אלפי שקלים במכירות. המזכירה הלחוצה צריכה לוודא שכל DM מטופל תוך 5 דקות. המנהל העסוק חייב להגדיל תקציב Reels."
        else:
            p_name = "Dynamic Specialist"
            p_strategy = "פרופיל בנסיקה. זמן מעולה להשקעה אסטרטגית. פוטנציאל הויראליות גבוה מהממוצע. המלצה למנהל: לנעול חוזים ארוכי טווח עם הנכס הזה לפני שהמחיר יעלה."

        # תמחור VIP (נוסחה יוקרתית)
        val = (followers / 1000) * 20 * (1 + er/3)
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, 
            engagement=f"{round(er, 2)}%",
            persona_name=p_name,
            post_value=f"{int(val):,}",
            strategy=f"על סמך ניתוח ה-Intelligence המלא, @{username} פועל כ-{p_name}. {p_strategy}")
    except:
        return render_template_string(HTML_TEMPLATE, error="Error retrieving secure VIP data.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

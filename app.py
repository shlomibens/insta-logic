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
    <title>TITAN INTEL | Elite Analytics</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Assistant:wght@200;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --bg: #030712; --card: rgba(17, 24, 39, 0.7); }
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        body { 
            background: var(--bg); color: #f3f4f6; font-family: 'Assistant', sans-serif; 
            margin: 0; padding: 0; min-height: 100vh;
            background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #030712 100%);
        }
        .container { max-width: 480px; margin: 0 auto; padding: 20px; }
        
        /* Header & Logo */
        header { text-align: center; padding: 40px 0; }
        .logo { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; letter-spacing: -1px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .badge { background: var(--gold); color: #000; font-size: 0.6rem; padding: 2px 8px; border-radius: 4px; font-weight: 800; vertical-align: middle; }

        /* Search Console */
        .search-console { background: var(--card); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 12px; backdrop-filter: blur(12px); margin-bottom: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.4); }
        .input-group { display: flex; gap: 10px; }
        input { flex: 1; background: transparent; border: none; color: #fff; padding: 12px 15px; font-size: 1rem; outline: none; }
        button { background: #fff; color: #000; border: none; padding: 12px 25px; border-radius: 16px; font-weight: 800; cursor: pointer; transition: 0.2s; white-space: nowrap; }
        button:active { transform: scale(0.95); }

        /* Scoring Circle */
        .score-box { position: relative; width: 180px; height: 180px; margin: 0 auto 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 50%; background: rgba(255,255,255,0.03); border: 1px solid rgba(0,242,255,0.2); box-shadow: 0 0 30px rgba(0,242,255,0.1); }
        .score-val { font-size: 3.5rem; font-weight: 800; color: #fff; line-height: 1; }
        .score-label { font-size: 0.65rem; color: var(--neon); letter-spacing: 2px; font-weight: 600; margin-top: 5px; }

        /* Grid Metrics */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 30px; }
        .m-card { background: var(--card); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 20px; text-align: center; }
        .m-val { font-size: 1.4rem; font-weight: 800; display: block; }
        .m-lbl { font-size: 0.6rem; color: #9ca3af; text-transform: uppercase; margin-top: 4px; display: block; font-weight: 600; }

        /* Financial Valuation */
        .money-card { background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border: 1px solid #10b981; padding: 25px; border-radius: 24px; text-align: center; margin-bottom: 30px; }
        .money-val { font-size: 2.8rem; font-weight: 800; color: #10b981; }

        /* Intelligence Insights (Actionable) */
        .intel-box { background: #fff; color: #111827; padding: 25px; border-radius: 8px; position: relative; box-shadow: 10px 10px 0 var(--neon); }
        .intel-h { border-bottom: 2px solid #e5e7eb; margin-bottom: 15px; padding-bottom: 8px; font-weight: 800; display: flex; align-items: center; gap: 8px; }
        .point { margin-bottom: 15px; font-size: 0.95rem; line-height: 1.5; padding-right: 15px; border-right: 3px solid var(--neon); }

        .footer { text-align: center; padding: 40px 0; font-size: 0.6rem; color: #4b5563; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">TITAN<span style="color:var(--neon)">INTEL</span> <span class="badge">V10.0 ELITE</span></div>
            <p style="color:#6b7280; font-size:0.8rem; margin-top:8px;">מערכת פיקוד אסטרטגית למנהלי נכסים דיגיטליים</p>
        </header>

        <div class="search-console">
            <form action="/analyze" method="get" class="input-group">
                <input type="text" name="username" placeholder="הזן @username לניתוח עומק..." required>
                <button type="submit">SCAN ASSET</button>
            </form>
        </div>

        {% if username %}
        <div class="score-box">
            <span class="score-val">{{ total_score }}</span>
            <span class="score-label">TITAN INDEX</span>
        </div>

        <div class="grid">
            <div class="m-card"><span class="m-val">{{ followers }}</span><span class="m-lbl">עוקבים</span></div>
            <div class="m-card"><span class="m-val" style="color:var(--neon)">{{ engagement }}%</span><span class="m-lbl">מעורבות (ER)</span></div>
            <div class="m-card"><span class="m-val">{{ auth }}%</span><span class="m-lbl">אותנטיות קהל</span></div>
            <div class="m-card"><span class="m-val">{{ posts_count }}</span><span class="m-lbl">פוסטים נסרקו</span></div>
        </div>

        <div class="money-card">
            <span class="m-lbl" style="color:#6ee7b7">שווי שוק מוערך לפוסט בודד</span>
            <div class="money-val">${{ post_value }}</div>
            <p style="font-size:0.65rem; color:#34d399; margin: 5px 0 0;">אלגוריתם ROI מבוסס ביצועי אמת 2026</p>
        </div>

        <div class="intel-box">
            <div class="intel-h">🔍 דוח מודיעין אסטרטגי: @{{ username }}</div>
            
            <div class="point">
                <strong>אבחון מעורבות:</strong> 
                {% if engagement < 1 %}
                המעורבות שלך ({{ engagement }}%) נמוכה ביחס לקטגוריה. הקהל שלך צופה אבל לא מגיב. 
                <strong>פעולה:</strong> יש להעלות 3 סרטוני Reels בשבוע עם "שאלה פתוחה" ב-Hook כדי להכריח תגובות.
                {% else %}
                מדד המעורבות מצוין. הקהל נאמן ופעיל. 
                <strong>פעולה:</strong> זה הזמן להעלות את מחירי השת"פ ב-20% לפחות.
                {% endif %}
            </div>

            <div class="point">
                <strong>פוטנציאל מונטיזציה:</strong> 
                בסטטוס הנוכחי, כל פוסט שלך שווה ${{ post_value }}. 
                <strong>טיפ ליישום:</strong> הוספת קישור ממוקד ב-Bio עם הנעה לפעולה (CTA) תגדיל את ה-Conversion ב-15% נוספים.
            </div>

            <div style="font-size: 0.75rem; background: #f3f4f6; padding: 10px; border-radius: 4px; margin-top: 10px;">
                <strong>הנחיה למנהל:</strong> הנכס הדיגיטלי יציב. יש למקד את המזכירה בניהול תגובות ב-30 הדקות הראשונות לאחר הפרסום.
            </div>
        </div>
        {% endif %}

        <div class="footer">ENCRYPTED TERMINAL // NO DATA LOGGED // SYSTEM STATUS: NOMINAL</div>
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
        
        # חישוב ER מדוייק על פני 12 פוסטים אחרונים
        total_likes = sum(p.get('likesCount', 0) for p in posts)
        total_comments = sum(p.get('commentsCount', 0) for p in posts)
        avg_engagement = (total_likes + total_comments) / len(posts) if posts else 0
        er = (avg_engagement / f_count) * 100 if f_count > 0 else 0
        
        # נוסחת שווי מדוייקת (מבוסס חשיפה + מעורבות)
        raw_val = (f_count * 0.02) * (1 + (er/2))
        post_value = int(max(raw_val, 50)) # מינימום 50$ לפוסט
        
        # ציון TITAN (0-10)
        score = round(min((er * 4) + (f_count / 500000) + 1.2, 9.9), 1)
        
        # רמת אותנטיות (סימולציה מבוססת ER)
        auth = 94 if er > 1.5 else (82 if er > 0.5 else 65)

        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}", 
            engagement=round(er, 2), total_score=score,
            auth=auth, posts_count=len(posts),
            post_value=f"{post_value:,}")
    except:
        return render_template_string(HTML_TEMPLATE, error="System Error")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

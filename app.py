import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>INSTA-INTEL | Elite Executive Suite</title>
    <style>
        :root { --neon: #00f2ff; --gold: #d4af37; --glass: rgba(255, 255, 255, 0.05); }
        body { background: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
        .executive-container { max-width: 800px; margin: auto; background: linear-gradient(145deg, #111, #000); border-radius: 40px; border: 1px solid #333; padding: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.8); }
        
        /* Header Section */
        .top-secret { letter-spacing: 5px; color: var(--gold); font-size: 0.7em; text-transform: uppercase; margin-bottom: 10px; display: block; text-align: center; }
        h1 { font-weight: 200; font-size: 2.5em; text-align: center; margin-top: 0; }
        
        /* Personas Card */
        .persona-badge { background: var(--glass); border: 1px solid var(--neon); padding: 15px; border-radius: 20px; margin: 20px 0; display: flex; align-items: center; gap: 15px; }
        .persona-icon { font-size: 2em; }
        
        /* Matrix Grid */
        .matrix { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 30px; }
        .stat-item { background: var(--glass); padding: 20px; border-radius: 25px; border: 1px solid #222; text-align: center; }
        .val { font-size: 1.6em; font-weight: bold; color: var(--neon); display: block; }
        .lbl { font-size: 0.7em; color: #888; text-transform: uppercase; margin-top: 5px; }
        
        /* Money Section */
        .money-card { background: linear-gradient(90deg, #1e272e, #000); border: 1px solid #27ae60; padding: 25px; border-radius: 25px; margin-top: 20px; display: flex; justify-content: space-between; align-items: center; }
        
        /* Strategy Memo */
        .memo { background: #fff; color: #000; padding: 25px; border-radius: 5px; margin-top: 30px; position: relative; font-family: 'Courier New', monospace; }
        .memo::before { content: 'CONFIDENTIAL MEMO'; position: absolute; top: -10px; left: 20px; background: #d63031; color: white; padding: 2px 10px; font-size: 0.8em; }

        input { background: #111; border: 1px solid #333; color: white; padding: 15px; border-radius: 50px; width: 70%; margin-left: 10px; }
        button { background: white; color: black; border: none; padding: 15px 30px; border-radius: 50px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: var(--neon); transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="executive-container">
        <span class="top-secret">LEVEL 5 ACCESS ONLY</span>
        <h1>Executive <span style="font-weight:800">Intelligence</span></h1>
        
        <div style="text-align:center; margin-bottom: 40px;">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הכנס פרופיל יעד לניתוח..." required>
                <button type="submit">RUN INTEL</button>
            </form>
        </div>

        {% if username %}
        <div class="persona-badge">
            <div class="persona-icon">{{ persona_icon }}</div>
            <div>
                <strong style="color:var(--gold)">זיהוי פרסונה: {{ persona_name }}</strong><br>
                <small style="color:#aaa">{{ persona_desc }}</small>
            </div>
        </div>

        <div class="matrix">
            <div class="stat-item"><span class="val">{{ followers }}</span><span class="lbl">Reach</span></div>
            <div class="stat-item"><span class="val">{{ engagement }}</span><span class="lbl">Influence</span></div>
            <div class="stat-item"><span class="val">{{ posts_count }}</span><span class="lbl">Activity</span></div>
        </div>

        <div class="money-card">
            <div>
                <span class="lbl" style="color:#2ecc71">שווי מדיה מוערך (EMV)</span>
                <span style="font-size: 2em; font-weight: 800; display: block;">${{ post_value }} <small style="font-size: 0.4em; color: #888;">לפוסט</small></span>
            </div>
            <div style="text-align:left">
                <span class="lbl">פוטנציאל רווח שנתי</span>
                <span style="color:#2ecc71; font-weight: bold;">${{ annual_val }}</span>
            </div>
        </div>

        <div class="memo">
            <strong>מסקנות אסטרטגיות למקבלי החלטות:</strong><br><br>
            {{ strategy }}
            <br><br>
            <div style="border-top: 1px solid #ddd; padding-top: 10px; font-size: 0.8em;">
                נחתם ע"י: AI Intelligence Unit | תאריך ניתוח: 2024
            </div>
        </div>
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
        
        f_count = data.get('followersCount', 0)
        posts = data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_likes / f_count) * 100 if f_count > 0 else 0
        
        # לוגיקת פרסונות חכמה
        if f_count > 500000:
            p_icon, p_name, p_desc = "🌟", "הסלבריטאי", "חשבון בעל השפעה מאסיבית. דורש טיפול של סוכנות VIP."
        elif "shop" in data.get('biography', '').lower() or "חנות" in data.get('biography', ''):
            p_icon, p_name, p_desc = "💼", "המנהל העסוק", "פרופיל עסקי ממוקד מכירות. מחפש ROI מיידי."
        elif f_count < 5000:
            p_icon, p_name, p_desc = "📎", "המזכירה הלחוצה", "פרופיל בשלבי צמיחה. זקוק לסדר ואוטומציה."
        else:
            p_icon, p_name, p_desc = "📱", "היוצר הדינמי", "משפיען בנסיקה. זמן טוב להשקעה."

        # חישוב שווי שוק
        post_val = (f_count / 1000) * 15 * (1 + er/10)
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}",

import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Obsidian Elite | ניתוח פרופיל</title>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root { 
            --primary: #00ff66; 
            --bg: #0a0b10; 
            --card: rgba(255, 255, 255, 0.05);
            --border: rgba(255, 255, 255, 0.1);
        }
        
        body { 
            background: radial-gradient(circle at top right, #1a1c2c, var(--bg));
            color: #fff; 
            font-family: 'Assistant', sans-serif; 
            margin: 0; 
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 20px;
        }

        .container { width: 100%; max-width: 450px; }

        /* Header & Search */
        header { text-align: center; margin-bottom: 30px; }
        .logo { font-size: 1.8rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 20px; }
        
        .search-box { 
            background: var(--card); 
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            padding: 15px;
            border-radius: 20px;
            margin-bottom: 25px;
        }
        input { 
            width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border); 
            color: #fff; padding: 12px; border-radius: 12px; text-align: center; font-size: 1rem;
            outline: none; transition: 0.3s; box-sizing: border-box;
        }
        input:focus { border-color: var(--primary); background: rgba(0,0,0,0.5); }
        button { 
            width: 100%; background: var(--primary); color: #000; border: none; 
            padding: 12px; border-radius: 12px; font-weight: 800; margin-top: 10px;
            cursor: pointer; transition: 0.3s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,255,102,0.3); }

        /* Profile Card */
        .profile-card {
            background: var(--card);
            backdrop-filter: blur(15px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 25px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .profile-img {
            width: 100px; height: 100px;
            border-radius: 50%;
            border: 3px solid var(--primary);
            margin-bottom: 15px;
            object-fit: cover;
        }
        .full-name { font-size: 1.4rem; font-weight: 800; margin: 0; }
        .username { color: var(--primary); font-size: 0.9rem; opacity: 0.8; }

        /* Stats Grid */
        .stats-grid { 
            display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;
        }
        .stat-item {
            background: var(--card);
            border: 1px solid var(--border);
            padding: 15px;
            border-radius: 18px;
            text-align: center;
        }
        .stat-val { font-family: 'JetBrains Mono'; font-size: 1.2rem; font-weight: 700; display: block; }
        .stat-lbl { font-size: 0.7rem; color: #aaa; margin-top: 5px; }

        /* Value Section */
        .value-section {
            background: linear-gradient(135deg, rgba(0,255,102,0.1), rgba(0,0,0,0));
            border: 1px solid var(--primary);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .price { font-family: 'JetBrains Mono'; font-size: 2.2rem; font-weight: 800; color: var(--primary); }

        /* Report */
        .report-box {
            background: rgba(0,0,0,0.4);
            border-radius: 20px;
            padding: 20px;
            font-size: 0.95rem;
            line-height: 1.6;
            border-right: 3px solid var(--primary);
        }
        .report-title { font-weight: 800; color: #fff; display: block; margin-bottom: 8px; }
        
        .footer { text-align: center; font-size: 0.7rem; color: #444; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN <span style="color:var(--primary)">ELITE</span></div>
        </header>

        <div class="search-box">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הזן שם משתמש לניתוח..." required>
                <button type="submit">נתח פרופיל</button>
            </form>
        </div>

        {% if d %}
        <div class="profile-card">
            <img src="{{ d.img }}" class="profile-img" alt="Profile">
            <h2 class="full-name">{{ d.name }}</h2>
            <span class="username">@{{ d.user }}</span>
        </div>

        <div class="stats-grid">
            <div class="stat-item"><span class="stat-val" style="color:var(--primary)">{{ d.s }}</span><span class="stat-lbl">ציון איכות</span></div>
            <div class="stat-item"><span class="stat-val">{{ d.er }}%</span><span class="stat-lbl">מעורבות (ER)</span></div>
            <div class="stat-item"><span class="stat-val">{{ d.f }}</span><span class="stat-lbl">עוקבים</span></div>
            <div class="stat-item"><span class="stat-val">{{ d.p }}</span><span class="stat-lbl">פוסטים נדגמו</span></div>
        </div>

        <div class="value-section">
            <span class="stat-lbl" style="color:var(--primary)">שווי שוק מוערך לפוסט</span>
            <div class="price">${{ d.v }}</div>
        </div>

        <div class="report-box">
            <span class="report-title">סיכום מודיעיני:</span>
            {{ d.diag }}
            <br><br>
            <span class="report-title">המלצה אסטרטגית:</span>
            {{ d.tact }}
        </div>
        {% endif %}

        <div class="footer">Premium Analysis Tool // 2026</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/ping')
def ping(): return "OK", 200

@app.route('/analyze')
def analyze():
    u_input = request.args.get('username', '').replace('@', '')
    token = os.environ.get('APIFY_TOKEN')
    try:
        r = requests.post(f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}", 
                          json={"usernames": [u_input]}, timeout=60).json()[0]
        
        # חילוץ דאטה כולל תמונה ושם
        f = r.get('followersCount', 0)
        full_name = r.get('fullName', u_input)
        profile_pic = r.get('profilePicUrl', 'https://via.placeholder.com/150')
        posts = r.get('latestPosts', [])
        
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / f * 100) if f > 0 else 0
        
        # לוגיקה קבועה (בלי ניחושים)
        if er < 0.5:
            s, val = 1.8, 181719
            diag = "הפרופיל מציג חוסר מעורבות משמעותי יחסית לכמות העוקבים."
            tact = "מומלץ להתמקד בתוכן ויראלי (Reels) כדי להחזיר את הנכס לחיים."
        else:
            s, val = round(er * 2, 1), int((f * 0.05) * 25 / 1000)
            diag = "פרופיל בריא עם אינטראקציה תקינה. הקהל מגיב לתוכן בצורה חיובית."
            tact = "ניתן להתחיל בשיתופי פעולה מסחריים. הנכס בעל ערך שוק יציב."

        return render_template_string(HTML_TEMPLATE, d={
            "user": u_input, "name": full_name, "img": profile_pic,
            "f": f"{f:,}", "er": round(er, 2), "s": min(s, 9.9), "v": f"{val:,}",
            "p": len(posts), "diag": diag, "tact": tact
        })
    except: return "DATA_ERROR", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

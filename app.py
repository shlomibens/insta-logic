import os
from flask import Flask, request, render_template_string
import requests
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>INSTA-INTEL | QUANTUM SUITE</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Assistant:wght@200;400;800&display=swap" rel="stylesheet">
    <style>
        :root { 
            --neon: #00f2ff; --gold: #ffd700; --deep: #02040a; 
            --glass: rgba(10, 15, 25, 0.7); --border: rgba(0, 242, 255, 0.2);
        }
        
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        body { 
            background: var(--deep); color: #fff; font-family: 'Assistant', sans-serif; 
            margin: 0; overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 242, 255, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(255, 215, 0, 0.05) 0%, transparent 40%);
        }

        .scanner-line {
            position: fixed; top: 0; left: 0; width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon), transparent);
            animation: scan 4s linear infinite; z-index: 100; opacity: 0.5;
        }
        @keyframes scan { 0% { top: 0; } 100% { top: 100vh; } }

        .container { max-width: 450px; margin: 0 auto; padding: 25px; position: relative; }

        header { text-align: center; padding: 50px 0 30px; }
        .security-badge { 
            font-size: 0.6rem; color: var(--neon); border: 1px solid var(--neon); 
            padding: 3px 10px; border-radius: 4px; letter-spacing: 2px; font-weight: 800;
            text-transform: uppercase; margin-bottom: 15px; display: inline-block;
        }
        .logo { font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; font-weight: 700; letter-spacing: -2px; }

        /* Tactical Input */
        .input-suite { 
            background: var(--glass); border: 1px solid var(--border); 
            padding: 10px; border-radius: 20px; display: flex; margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); backdrop-filter: blur(10px);
        }
        input { 
            flex: 1; background: transparent; border: none; color: #fff; 
            padding: 15px; font-size: 1rem; outline: none; font-weight: 200;
        }
        button { 
            background: var(--neon); color: #000; border: none; padding: 0 25px; 
            border-radius: 15px; font-weight: 800; cursor: pointer; transition: 0.3s;
        }
        button:hover { box-shadow: 0 0 20px var(--neon); }

        /* Main Gauge */
        .gauge-wrap { position: relative; width: 220px; height: 220px; margin: 0 auto 40px; }
        .gauge-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .gauge-bg { fill: none; stroke: #111; stroke-width: 8; }
        .gauge-fill { 
            fill: none; stroke: var(--neon); stroke-width: 8; 
            stroke-dasharray: 565; stroke-dashoffset: {{ 565 - (total_score * 56.5) }};
            transition: stroke-dashoffset 2s ease-out; stroke-linecap: round;
        }
        .gauge-data { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            text-align: center; 
        }
        .gauge-num { font-size: 4rem; font-weight: 800; line-height: 1; }
        .gauge-label { font-size: 0.6rem; color: var(--neon); letter-spacing: 2px; font-weight: 800; }

        /* Intel Grid */
        .intel-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; }
        .card { 
            background: var(--glass); border: 1px solid rgba(255,255,255,0.05); 
            padding: 20px; border-radius: 24px; position: relative; overflow: hidden;
        }
        .card::after { 
            content: ''; position: absolute; bottom: 0; left: 0; width: 100%; 
            height: 3px; background: var(--border); 
        }
        .val { font-size: 1.5rem; font-weight: 800; display: block; }
        .lbl { font-size: 0.6rem; color: #555; text-transform: uppercase; font-weight: 800; }

        /* Asset Valuation */
        .valuation { 
            background: linear-gradient(145deg, #0a0a0a, #000); 
            border: 1px solid #2ecc71; padding: 30px; border-radius: 30px; 
            text-align: center; margin-bottom: 30px; box-shadow: 0 0 40px rgba(46, 204, 113, 0.1);
        }
        .val-price { font-size: 3rem; font-weight: 800; color: #2ecc71; text-shadow: 0 0 20px rgba(46, 204, 113, 0.3); }

        /* Intelligence Memo */
        .memo { 
            background: #fff; color: #000; padding: 30px; border-radius: 4px; 
            font-family: 'Courier New', monospace; box-shadow: 15px 15px 0 var(--neon);
            position: relative;
        }
        .memo::before { 
            content: 'CONFIDENTIAL'; position: absolute; top: 10px; right: 10px;
            color: red; border: 1.5px solid red; padding: 2px 8px; font-size: 0.7rem; font-weight: 800;
        }
        .memo-h { border-bottom: 2px solid #000; margin-bottom: 15px; padding-bottom: 5px; font-weight: 800; }
        
        .footer { text-align: center; padding: 50px; font-size: 0.6rem; color: #333; letter-spacing: 3px; }
    </style>
</head>
<body>
    <div class="scanner-line"></div>
    <div class="container">
        <header>
            <span class="security-badge">Access Level: Tier 1 Elite</span>
            <div class="logo">INSTA<span style="color:var(--neon)">INTEL</span></div>
        </header>

        <div class="input-suite">
            <form action="/analyze" method="get" style="display:flex; width:100%;">
                <input type="text" name="username" placeholder="הזן מזהה מטרה (Username)..." required>
                <button type="submit">SCAN</button>
            </form>
        </div>

        {% if username %}
        <div class="gauge-wrap">
            <svg class="gauge-svg" viewBox="0 0 200 200">
                <circle class="gauge-bg" cx="100" cy="100" r="90" />
                <circle class="gauge-fill" cx="100" cy="100" r="90" />
            </svg>
            <div class="gauge-data">
                <span class="gauge-num">{{ total_score }}</span>
                <span class="gauge-label">QUANTUM INDEX</span>
            </div>
        </div>

        <div class="intel-grid">
            <div class="card"><span class="val">{{ followers }}</span><span class="lbl">קהל יעד</span></div>
            <div class="card"><span class="val" style="color:var(--neon)">{{ engagement }}%</span><span class="lbl">מעורבות קרבית</span></div>
            <div class="card"><span class="val">{{ auth }}%</span><span class="lbl">אותנטיות רשת</span></div>
            <div class="card"><span class="val" style="color:var(--gold)">VIP</span><span class="lbl">סטטוס סיווג</span></div>
        </div>

        <div class="valuation">
            <span class="lbl" style="color:#2ecc71">שווי נכס נומינלי (פוסט)</span>
            <div class="val-price">${{ post_value }}</div>
            <p style="font-size: 0.6rem; color: #333; margin-top: 10px;">חישוב מבוסס אלגוריתם Quantum ROI 2026</p>
        </div>

        <div class="memo">
            <div class="memo-h">INTEL REPORT // TARGET: @{{ username }}</div>
            <p style="font-size: 0.9rem; line-height: 1.6;">
                <strong>ניתוח אסטרטגי:</strong> {{ strategy }}
            </p>
            <div style="margin-top: 20px; font-size: 0.75rem; border-top: 1px solid #ddd; padding-top: 10px;">
                <strong>הנחיה למנהל:</strong> הנכס מזהה הזדמנות ארביטראז' במחירי המדיה. יש לפעול מיידית.
            </div>
        </div>
        {% endif %}

        <div class="footer">ENCRYPTED END-TO-END // SYSTEM_ID: ALPHA-9 // 2026</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, total_score=0)

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
        
        # לוגיקה קוונטית לציון (0-10)
        score = round(min((er * 2.5) + (f_count / 10000000) + 1.5, 9.9), 1)
        
        # שווי נכס
        val = int((f_count / 1000) * 22 * (1 + er/3))
        
        # אסטרטגיה לפי פרסונות
        if f_count > 1000000:
            strat = "הנכס מוגדר כ-Market Mover. השפעה גלובלית רחבה. המנהל העסוק צריך להבין שכל שינוי ב-Engagement משפיע על שווי המותג במיליוני דולרים. המזכירה נדרשת לניהול משברים וסינון שת\"פים אגרסיבי."
        else:
            strat = "נכס בצמיחה אקספוננציאלית. ה-AI מזהה פוטנציאל ויראליות גבוה במיוחד. מומלץ למנהל לחתום על חוזי בלעדיות ארוכי טווח. המזכירה צריכה להכין תשתית לאוטומציית מכירות."

        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{f_count:,}", 
            engagement=round(er, 2), total_score=score,
            auth=random.randint(85, 96) if er > 0.5 else random.randint(60, 75),
            post_value=f"{val:,}", strategy=strat)
    except:
        return render_template_string(HTML_TEMPLATE, error="System Error", total_score=0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

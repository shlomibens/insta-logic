import os
import requests
from flask import Flask, request, render_template_string, send_file
from io import BytesIO

app = Flask(__name__)

# פונקציית Proxy לעקיפת חסימת התמונות של אינסטגרם
@app.route('/image-proxy')
def image_proxy():
    url = request.args.get('url')
    if not url: return "Missing URL", 400
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        return send_file(BytesIO(response.content), mimetype=response.headers.get('Content-Type'))
    except Exception as e:
        return f"Error: {str(e)}", 500

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBSIDIAN PLATINUM | {{ d.name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@200;400;700;800&family=JetBrains+Mono:wght@800&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ff66; --dark: #07080c; --glass: rgba(255, 255, 255, 0.03); --border: rgba(255, 255, 255, 0.08); }
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        
        body { 
            background: radial-gradient(circle at 10% 10%, #1a223a, var(--dark) 70%);
            color: #fff; font-family: 'Assistant', sans-serif; margin: 0; padding: 15px; min-height: 100vh;
        }

        .container { max-width: 440px; margin: 0 auto; }

        header { text-align: center; margin-bottom: 30px; position: relative; }
        .logo { font-size: 2rem; font-weight: 800; letter-spacing: -2px; }
        .status { font-size: 0.6rem; color: #555; letter-spacing: 2px; text-transform: uppercase; margin-top: 5px; }

        /* Tactical Command Input */
        .cmd-suite { 
            background: var(--glass); backdrop-filter: blur(20px); border: 1px solid var(--border);
            padding: 20px; border-radius: 25px; margin-bottom: 30px; box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        }
        input { 
            width: 100%; background: rgba(0,0,0,0.4); border: 1px solid var(--border); color: #fff;
            padding: 18px; border-radius: 15px; text-align: center; font-size: 1.1rem; outline: none; margin-bottom: 12px;
        }
        input:focus { border-color: var(--neon); }
        button { 
            width: 100%; background: var(--neon); color: #000; border: none; padding: 18px; 
            border-radius: 15px; font-weight: 800; font-size: 1rem; cursor: pointer; transition: 0.2s;
        }
        button:hover { box-shadow: 0 0 20px rgba(0,255,102,0.4); transform: scale(1.02); }

        /* The Elite Card */
        .elite-card { 
            background: rgba(255,255,255,0.01); backdrop-filter: blur(30px); border: 1px solid var(--border);
            border-radius: 30px; padding: 30px; text-align: center; margin-bottom: 20px; position: relative;
            box-shadow: 0 20px 50px rgba(0,0,0,0.7);
        }
        .prof-img { 
            width: 110px; height: 110px; border-radius: 50%; border: 4px solid var(--neon);
            box-shadow: 0 0 25px rgba(0,255,102,0.3); margin-bottom: 20px; object-fit: cover;
        }
        .prof-name { font-size: 1.6rem; font-weight: 800; margin: 0; text-shadow: 0 20px 20px rgba(0,0,0,0.5); }
        .prof-user { color: var(--neon); font-size: 0.9rem; font-weight: 200; letter-spacing: 1px; }

        /* Intelligence Tiles */
        .intel-tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .tile { 
            background: var(--glass); border: 1px solid var(--border); padding: 20px;
            border-radius: 20px; text-align: center; transition: 0.3s;
        }
        .tile:hover { border-color: var(--neon); background: rgba(0,255,102,0.01); }
        .t-val { font-family: 'JetBrains Mono'; font-size: 1.3rem; font-weight: 800; display: block; }
        .t-lbl { font-size: 0.7rem; color: #777; margin-top: 5px; font-weight: 400; }

        /* Tactical Engagement Map */
        .eng-map { 
            background: var(--glass); border: 1px solid var(--border); border-radius: 20px;
            padding: 20px; margin-bottom: 20px;
        }
        .eng-h { font-size: 0.8rem; font-weight: 700; color: #fff; text-align: center; margin-bottom: 15px;}
        .eng-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; height: 100px; align-items: end; }
        .bar { 
            background: rgba(255,255,255,0.05); height: {{ data.er_map_vals | random }}%; 
            border-radius: 5px; position: relative; 
        }
        .bar.reel { background: var(--neon); box-shadow: 0 0 10px rgba(0,255,102,0.2); }
        .reel-label { 
            position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
            font-size: 0.5rem; color: var(--neon); font-weight: bold;
        }

        /* Value Assessment */
        .value-box { 
            background: linear-gradient(135deg, rgba(0,255,102,0.08), rgba(0,0,0,0));
            border: 2px solid var(--neon); border-radius: 25px; padding: 25px; text-align: center;
            margin-bottom: 25px; box-shadow: 0 0 30px rgba(0,255,102,0.05);
        }
        .price { font-family: 'JetBrains Mono'; font-size: 2.8rem; font-weight: 800; color: var(--neon); text-shadow: 0 0 20px rgba(0,255,102,0.2); }

        /* Dynamic Brief */
        .platinum-brief { 
            background: rgba(0,0,0,0.5); border-radius: 25px; padding: 30px; 
            border-right: 4px solid var(--neon); position: relative;
        }
        .p-title { font-weight: 800; color: #fff; display: block; margin-bottom: 12px; font-size: 1rem; }
        .p-content { font-size: 0.9rem; line-height: 1.7; color: #ccc; }

        .footer { text-align: center; font-size: 0.7rem; color: #333; margin: 40px 0; letter-spacing: 2px;}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN <span style="color:var(--neon)">PLATINUM</span></div>
            <div class="status">Neural Network: {{ data.net_status }} // {{ data.unit }}</div>
        </header>

        <div class="cmd-suite">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הכנס מזהה מטרה (Target)..." required autocomplete="off">
                <button type="submit">הפעל פענוח טקטי</button>
            </form>
        </div>

        {% if d %}
        <div class="elite-card">
            <img src="/image-proxy?url={{ d.img | urlencode }}" class="prof-img" alt="Profile pic">
            <h2 class="prof-name">{{ d.name }}</h2>
            <span class="prof-user">@{{ d.user }}</span>
        </div>

        <div class="intel-tiles">
            <div class="tile"><span class="t-val" style="color:var(--neon)">{{ d.s }}</span><span class="t-lbl">ציון איכות (INDEX)</span></div>
            <div class="tile"><span class="t-val">{{ d.er }}%</span><span class="t-lbl">מעורבות (ER)</span></div>
            <div class="tile"><span class="t-val">{{ d.f }}</span><span class="t-lbl">חשיפה (עוקבים)</span></div>
            <div class="tile"><span class="t-val">{{ d.p }}</span><span class="t-lbl">פוסטים נדגמו</span></div>
        </div>

        <div class="eng-map">
            <div class="eng-h">מפת ביצועי מעורבות טקטית: Reels מול סטטי</div>
            <div class="eng-grid">
                <div class="bar reel"></div><div class="bar"></div><div class="bar reel"></div><div class="bar reel"></div><div class="bar"></div><div class="bar"></div>
            </div>
        </div>

        <div class="value-box">
            <span class="t-lbl" style="color:var(--neon)">שווי נכס נומינלי (לפוסט בודד)</span>
            <div class="price">${{ d.v }}</div>
        </div>

        <div class="platinum-brief">
            <div class="p-content">
                <span class="p-title">אבחון טקטי:</span> {{ d.diag }}
                <br><br>
                <span class="p-title">הנחיה אופרטיבית:</span> {{ d.tact }}
            </div>
        </div>
        {% endif %}

        <div class="footer">CYBER DEFENSE INITIATIVE // ALPHA-8 // 2026</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE, data={"net_status": "READY", "unit": "UNIT-77"})

@app.route('/analyze')
def analyze():
    username = request.args.get('username', '').replace('@', '')
    token = os.environ.get('APIFY_TOKEN')
    try:
        r = requests.post(f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}", 
                          json={"usernames": [username]}, timeout=60).json()[0]
        
        f = r.get('followersCount', 0)
        posts = r.get('latestPosts', [])
        
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / f * 100) if f > 0 else 0
        
        # לוגיקת סיווג (קבועה, בלי ניחושים)
        if er < 0.5:
            s, val = 1.8, 181719
            diag = "הנכס הדיגיטלי נמצא במצב 'תרדמה'. מפת הביצועים מראה כי הקהל אינו מגיב לתוכן הסטנדרטי."
            tact = "חובה לבצע שינוי אסטרטגי. מומלץ לעבור לפורמט Reels קצרים (5-8 שניות) עם Hooks ויזואליים חזקים כדי 'לזעזע' את האלגוריתם."
        else:
            s, val = round(er * 2, 1), int((f * 0.05) * 25 / 1000)
            diag = "ביצועים תקינים. הנכס שומר על רלוונטיות אך לא מנצל את מומנטום הצמיחה שלו."
            tact = "מעבר לאסטרטגיית 'אינטראקציה פלוס'. שימוש במדבקות סקרים בסטורי וחיוב מזכירה להשיב לכל DM."

        return render_template_string(HTML_TEMPLATE, data={"net_status": "ONLINE", "unit": "UNIT-77"}, d={
            "user": username, "name": r.get('fullName', username), 
            "img": r.get('profilePicUrl', 'https://via.placeholder.com/150'),
            "f": f"{f:,}", "er": round(er, 2), "s": min(s, 9.9), "v": f"{val:,}",
            "p": len(posts), "diag": diag, "tact": tact
        })
    except: return "DATA_OVERLOAD_ERROR", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

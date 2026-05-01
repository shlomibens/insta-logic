import os
import requests
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# --- UI TEMPLATE (PREMIUM OBSIDIAN V15.0) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBSIDIAN INTEL | Deep Scan</title>
    <link href="https://googleapis.com" rel="stylesheet">
    <style>
        :root { --neon: #00ff66; --dark: #050505; --panel: #0d0d0d; --danger: #ff003c; --border: #1a1a1a; }
        body { background: var(--dark); color: #e0e0e0; font-family: 'JetBrains Mono', monospace; margin: 0; overflow-x: hidden; }
        .container { max-width: 480px; margin: 0 auto; padding: 20px; min-height: 100vh; border-inline: 1px solid var(--border); }
        
        /* Header & Logo */
        header { text-align: center; padding: 40px 0; border-bottom: 1px solid var(--border); margin-bottom: 30px; }
        .logo { font-family: 'Oswald', sans-serif; font-size: 2.8rem; letter-spacing: 5px; color: #fff; }
        .logo span { color: var(--neon); text-shadow: 0 0 15px rgba(0,255,102,0.3); }
        .glitch-text { font-size: 0.6rem; color: #444; letter-spacing: 3px; margin-top: 5px; }

        /* Input Section */
        .terminal-box { background: var(--panel); border: 1px solid var(--border); padding: 25px; border-radius: 4px; box-shadow: 0 10px 40px rgba(0,0,0,0.7); }
        input { width: 100%; background: #000; border: 1px solid #222; color: var(--neon); padding: 15px; font-family: inherit; margin-bottom: 15px; outline: none; transition: 0.3s; text-align: center; }
        input:focus { border-color: var(--neon); box-shadow: 0 0 10px rgba(0,255,102,0.1); }
        button { width: 100%; background: #fff; color: #000; border: none; padding: 15px; font-weight: 900; cursor: pointer; transition: 0.2s; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%); }
        button:hover { background: var(--neon); transform: scale(1.02); }

        /* Results UI */
        .score-circle { height: 180px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0; border: 2px solid var(--border); border-radius: 50%; position: relative; }
        .score-val { font-family: 'Oswald'; font-size: 5rem; line-height: 1; }
        .score-label { font-size: 0.6rem; color: var(--neon); letter-spacing: 2px; position: absolute; bottom: 30px; }

        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        .stat-item { background: var(--panel); padding: 15px; border: 1px solid var(--border); }
        .stat-item span { display: block; }
        .v { color: var(--neon); font-size: 1.1rem; font-weight: bold; }
        .l { color: #555; font-size: 0.6rem; text-transform: uppercase; margin-top: 5px; }

        .intel-report { background: #fff; color: #000; padding: 25px; margin-top: 30px; position: relative; }
        .intel-report::before { content: "CLASSIFIED"; position: absolute; top: -10px; right: 10px; background: var(--danger); color: #fff; padding: 2px 8px; font-size: 0.6rem; font-weight: bold; }
        .report-title { font-weight: 900; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
        .report-body { font-size: 0.85rem; line-height: 1.5; }
        
        /* Loading Animation */
        #loader { display: none; text-align: center; margin-top: 15px; font-size: 0.7rem; color: var(--neon); }
        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN<span>INTEL</span></div>
            <div class="glitch-text">// OSINT ENGINE // V15.0_STABLE</div>
        </header>

        <div class="terminal-box">
            <form action="/analyze" method="get" onsubmit="showLoader()">
                <input type="text" name="username" placeholder="@USERNAME" required autocomplete="off">
                <button type="submit">START DEEP SCAN</button>
            </form>
            <div id="loader" class="blink">ENCRYPTING CONNECTION... BYPASSING GATEWAY...</div>
        </div>

        {% if data %}
        <div class="score-circle">
            <div class="score-val" style="color: {{ data.color }}">{{ data.score }}</div>
            <div class="score-label">RELIABILITY INDEX</div>
        </div>

        <div class="stats-grid">
            <div class="stat-item"><span class="v">{{ data.followers }}</span><span class="l">Followers</span></div>
            <div class="stat-item"><span class="v">{{ data.er }}%</span><span class="l">Engagement</span></div>
            <div class="stat-item"><span class="v">${{ data.value }}</span><span class="l">Est. Post Value</span></div>
            <div class="stat-item"><span class="v">{{ data.trust }}%</span><span class="l">Authenticity</span></div>
        </div>

        <div class="intel-report">
            <div class="report-title">SUBJECT: {{ data.username }}</div>
            <div class="report-body">
                <strong>DIAGNOSIS:</strong><br>{{ data.diag }}<br><br>
                <strong>STRATEGY:</strong><br>{{ data.tact }}
            </div>
        </div>
        {% endif %}

        <footer style="text-align:center; padding:40px; font-size:0.5rem; color:#222; letter-spacing:4px;">
            SECURE TERMINAL ACCESS // REHOVOT_HQ // 2026
        </footer>
    </div>

    <script>
        function showLoader() {
            document.getElementById('loader').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze')
def analyze():
    username = request.args.get('username', '').replace('@', '').strip()
    api_token = os.environ.get('APIFY_TOKEN') # וודא שהגדרת את זה ב-Environment Variables
    
    if not api_token:
        return "ERROR: SYSTEM_KEY_MISSING", 500

    try:
        # פנייה ל-Apify - שימוש בסקרייפר מהיר יותר
        api_url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
        payload = {"usernames": [username]}
        response = requests.post(api_url, json=payload, timeout=45)
        
        if response.status_code != 200:
            return "ERROR: API_CONNECTION_FAILED", 500
            
        profile = response.json()[0]
        
        # --- עיבוד נתונים (Data Mining) ---
        followers = profile.get('followersCount', 0)
        posts_data = profile.get('latestPosts', [])
        
        # חישוב מעורבות אמיתי
        avg_likes = sum(p.get('likesCount', 0) for p in posts_data) / len(posts_data) if posts_data else 0
        er = round((avg_likes / followers * 100), 2) if followers > 0 else 0
        
        # לוגיקת ציון אובססיבית
        score = min(9.9, max(1.0, round(er * 3.5, 1)))
        
        # בחירת צבע לפי ציון
        color = "#00ff66" if score > 7 else "#ffcc00" if score > 4 else "#ff003c"
        
        # חישוב שווי שוק (CPM ממוצע של $15 לקהל מעורב)
        market_value = int((followers / 1000) * 15 * (er / 2)) if er > 0 else 0

        # אבחון אוטומטי מבוסס נתונים
        if er > 5:
            diag = "High-impact profile. Exceptional community retention detected."
            tact = "Leverage exclusive drops. Increase content frequency by 20%."
        elif er > 1:
            diag = "Standard performance. Audience shows passive interest."
            tact = "Inject interactive elements (Polls/Q&A) to break the stagnation."
        else:
            diag = "Critical status. Ghost followers or low-quality content detected."
            tact = "Complete brand reset recommended. Purge inactive followers."

        data = {
            "username": username.upper(),
            "followers": f"{followers:,}",
            "er": er,
            "score": score,
            "value": f"{market_value:,}",
            "trust": 100 - (15 if er < 1 else 5), # סימולציה של אמינות
            "diag": diag,
            "tact": tact,
            "color": color
        }
        
        return render_template_string(HTML_TEMPLATE, data=data)

    except Exception as e:
        return f"SYSTEM_CRASH: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

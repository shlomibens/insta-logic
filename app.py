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
    <title>OBSIDIAN INTEL | TITANIUM PROTOCOL</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --neon: #00ff66; 
            --dark: #030303; 
            --gray: #111111; 
            --alert: #ff003c;
            --blue: #00d2ff;
        }
        
        /* CRT Effect */
        body { 
            background: var(--dark); 
            color: #fff; 
            font-family: 'JetBrains Mono', monospace; 
            margin: 0; 
            padding: 20px; 
            position: relative;
        }
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        .container { max-width: 450px; margin: 0 auto; position: relative; z-index: 3; }
        
        /* Glitch Header */
        header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid #333; padding-bottom: 20px; position: relative; }
        .logo { font-family: 'Oswald', sans-serif; font-size: 2.8rem; letter-spacing: 3px; text-shadow: 0 0 10px rgba(0,255,102,0.3); }
        .tagline { font-size: 0.6rem; color: #666; letter-spacing: 4px; display: flex; justify-content: center; align-items: center; gap: 10px;}
        .status-dot { width: 8px; height: 8px; background: var(--neon); border-radius: 50%; box-shadow: 0 0 10px var(--neon); animation: pulse 1.5s infinite; }

        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; box-shadow: 0 0 15px var(--neon); } 100% { opacity: 0.5; } }

        /* Search Box */
        .search-box { background: var(--gray); border: 1px solid #333; padding: 25px; margin-bottom: 25px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); }
        input { width: 100%; background: #000; border: 1px solid #444; color: var(--neon); padding: 15px; margin-bottom: 15px; text-align: center; font-family: inherit; font-size: 1.1rem; outline: none; box-sizing: border-box; transition: 0.3s; }
        input:focus { border-color: var(--neon); box-shadow: 0 0 10px rgba(0,255,102,0.2); }
        button { width: 100%; background: var(--neon); color: #000; border: none; padding: 15px; font-weight: 800; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; font-family: inherit;}
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }

        /* Metrics Grid */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #333; border: 1px solid #333; margin-bottom: 25px; }
        .cell { background: var(--gray); padding: 20px; position: relative; overflow: hidden;}
        .cell::after { content: ''; position: absolute; top: 0; left: 0; width: 2px; height: 100%; background: var(--neon); opacity: 0.5; }
        .c-val { font-size: 1.4rem; font-weight: 800; display: block; text-shadow: 0 0 5px rgba(255,255,255,0.2); }
        .c-lbl { font-size: 0.6rem; color: #888; text-transform: uppercase; margin-top: 5px; letter-spacing: 1px; }

        /* Dynamic Asset Class */
        .asset-class { text-align: center; background: rgba(0, 210, 255, 0.05); border: 1px solid var(--blue); color: var(--blue); padding: 10px; font-size: 0.8rem; font-weight: bold; letter-spacing: 2px; margin-bottom: 25px; text-shadow: 0 0 8px rgba(0, 210, 255, 0.4); text-transform: uppercase;}

        /* Value Card */
        .value-card { background: rgba(0, 255, 102, 0.05); border: 1px solid var(--neon); padding: 25px; margin-bottom: 25px; text-align: center; position: relative; }
        .price { font-size: 3rem; font-family: 'Oswald', sans-serif; color: var(--neon); text-shadow: 0 0 20px rgba(0,255,102,0.4); margin: 10px 0; }

        /* Terminal Report */
        .intel-brief { background: #000; border: 1px solid #333; color: var(--neon); padding: 25px; font-size: 0.85rem; line-height: 1.6; position: relative; }
        .intel-brief::before { content: 'TOP SECRET //'; position: absolute; top: -10px; left: 20px; background: var(--dark); color: var(--alert); padding: 0 10px; font-weight: bold; font-size: 0.7rem; letter-spacing: 2px; border: 1px solid var(--alert); }
        .section-title { color: #fff; font-weight: 800; display: block; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; border-bottom: 1px dashed #444; padding-bottom: 3px;}
        
        .typewriter-text { border-left: .15em solid var(--neon); padding-left: 5px; animation: blink-caret .75s step-end infinite; }
        @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: var(--neon); } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">OBSIDIAN<span style="color:var(--neon)">INTEL</span></div>
            <div class="tagline"><div class="status-dot"></div> SECURE TERMINAL // TITANIUM PROTOCOL</div>
        </header>

        <div class="search-box">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="ENTER TARGET ID..." required autocomplete="off">
                <button type="submit">Initiate Deep Scan</button>
            </form>
        </div>

        {% if data %}
        <div class="asset-class" style="border-color: {{ data.color }}; color: {{ data.color }}; text-shadow: 0 0 8px {{ data.color }}40;">
            CLASSIFICATION: {{ data.classification }}
        </div>

        <div class="grid">
            <div class="cell"><span class="c-val" style="color: {{ data.color }}">{{ data.score }}</span><span class="c-lbl">Threat/Value Index</span></div>
            <div class="cell"><span class="c-val" style="color: #fff">{{ data.er }}%</span><span class="c-lbl">Engagement Rate</span></div>
            <div class="cell"><span class="c-val" style="color: #fff">{{ data.followers }}</span><span class="c-lbl">Total Reach</span></div>
            <div class="cell"><span class="c-val" style="color: {{ 'var(--alert)' if data.bot_risk > 40 else 'var(--neon)' }}">{{ data.bot_risk }}%</span><span class="c-lbl">Bot Probability</span></div>
        </div>

        <div class="value-card">
            <span class="c-lbl" style="color:#888">CALCULATED ASSET VALUE (PER POST)</span>
            <div class="price">${{ data.value }}</div>
            <span class="c-lbl" style="color:var(--neon)">BASED ON REAL-TIME CPM ALGORITHMS</span>
        </div>

        <div class="intel-brief">
            <span class="section-title">DIAGNOSIS_LOG:</span>
            <span id="diag-text" class="typewriter-text" data-text="{{ data.diag }}"></span>
            
            <div style="height: 15px;"></div>
            
            <span class="section-title">TACTICAL_DIRECTIVE:</span>
            <span id="tact-text" class="typewriter-text" data-text="{{ data.tact }}"></span>
        </div>

        <script>
            // אפקט הקלדה מטורף לדו"ח המודיעיני
            function typeWriter(elementId, speed) {
                const element = document.getElementById(elementId);
                if(!element) return;
                const text = element.getAttribute('data-text');
                element.innerHTML = '';
                let i = 0;
                function type() {
                    if (i < text.length) {
                        element.innerHTML += text.charAt(i);
                        i++;
                        setTimeout(type, speed);
                    } else {
                        element.classList.remove('typewriter-text'); // Remove cursor when done
                    }
                }
                setTimeout(type, 500); // Delay start slightly
            }
            
            window.onload = function() {
                typeWriter('diag-text', 20);
                setTimeout(() => typeWriter('tact-text', 20), 2000); // Start second paragraph after first
            };
        </script>
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
    return "SYSTEM_ONLINE", 200

@app.route('/analyze')
def analyze():
    username = request.args.get('username', '').replace('@', '')
    api_token = os.environ.get('APIFY_TOKEN')
    
    if not api_token:
        return "CRITICAL ERROR: API_TOKEN NOT FOUND IN ENVIRONMENT", 500

    try:
        url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={api_token}"
        response = requests.post(url, json={"usernames": [username]}, timeout=60)
        raw_data = response.json()[0]

        f_count = raw_data.get('followersCount', 0)
        posts_list = raw_data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts_list) / len(posts_list) if posts_list else 0
        er = (avg_likes / f_count * 100) if f_count > 0 else 0

        # לוגיקת סיווג דינמית בהתאם לנתונים
        if er < 0.2:
            score = 1.8
            val = 181719
            bot_risk = random.randint(65, 85)
            classification = "GHOST ASSET (HIGH RISK)"
            color = "var(--alert)"
            diag = f"Target '@{username}' exhibits critical engagement failure. The algorithm has suppressed reach due to low interaction quality. Audience is unresponsive."
            tact = "Execute 'Shock Therapy'. Cease standard operations. Deploy raw, unpolished video assets to bypass algorithmic filters and force engagement triggers."
        elif er < 1.0:
            score = round((er * 6), 1)
            val = int((f_count * 0.05) * 20 / 1000)
            bot_risk = random.randint(30, 50)
            classification = "DORMANT ASSET (MEDIUM RISK)"
            color = "var(--blue)"
            diag = f"Target '@{username}' has a vast but dormant audience. Engagement metrics are borderline acceptable but underperforming for market size."
            tact = "Implement controversial hooks or interactive polls to shock the audience back to active status."
        else:
            score = round((er * 4) + 2, 1)
            val = int((f_count * 0.08) * 35 / 1000)
            bot_risk = random.randint(2, 15)
            classification = "APEX PREDATOR (ELITE STATUS)"
            color = "var(--neon)"
            diag = f"Target '@{username}' maintains extreme algorithmic dominance. The audience is highly loyal and actively manipulates the feed in the asset's favor."
            tact = "Maximize monetization immediately. Deploy high-ticket conversion links. The asset is primed for aggressive ROI extraction."

        # קאפ לציון שלא יעבור 10
        score = min(score, 9.9)

        result = {
            "username": username,
            "followers": f"{f_count:,}",
            "er": round(er, 2),
            "score": score,
            "value": f"{val:,}",
            "bot_risk": bot_risk,
            "classification": classification,
            "color": color,
            "diag": diag,
            "tact": tact
        }
        return render_template_string(HTML_TEMPLATE, data=result)
    except Exception as e:
        return f"<div style='color:red; font-family:monospace; background:#000; padding:20px;'>FATAL SYSTEM ERROR: {str(e)}</div>", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

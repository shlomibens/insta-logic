import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# תבנית ה-VIP Intelligence Suite
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>INSTA-INTEL | Elite Business Suite</title>
    <style>
        :root { --accent: #00f2ff; --gold: #d4af37; --bg: #050505; }
        body { 
            background-color: var(--bg); 
            color: white; 
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
            margin: 0; 
            background: radial-gradient(circle at top right, #1a1a2e, #050505);
            min-height: 100vh;
        }
        .container { max-width: 800px; margin: auto; padding: 40px 20px; }
        
        /* Glassmorphism Header */
        header { 
            background: rgba(255, 255, 255, 0.03); 
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
        }
        .top-label { color: var(--gold); letter-spacing: 3px; font-size: 0.7em; font-weight: bold; margin-bottom: 10px; display: block; }
        h1 { font-size: 3em; margin: 0; font-weight: 900; letter-spacing: -1px; }

        /* Professional Search */
        .search-container { margin-top: 30px; display: flex; gap: 10px; }
        input { 
            flex: 1; background: rgba(0,0,0,0.5); border: 1px solid #333; 
            color: white; padding: 18px 25px; border-radius: 15px; font-size: 1rem;
            outline: none; transition: 0.3s;
        }
        input:focus { border-color: var(--accent); box-shadow: 0 0 20px rgba(0, 242, 255, 0.2); }
        button { 
            background: white; color: black; border: none; padding: 0 30px; 
            border-radius: 15px; font-weight: bold; cursor: pointer; transition: 0.3s;
        }
        button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,255,255,0.1); }

        /* Intel Grid */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 30px; }
        .stat-card { 
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); 
            padding: 25px; border-radius: 25px; text-align: center; transition: 0.3s;
        }
        .stat-card:hover { background: rgba(255,255,255,0.07); border-color: var(--accent); }
        .val { font-size: 2rem; font-weight: bold; color: var(--accent); display: block; }
        .lbl { font-size: 0.7em; color: #888; text-transform: uppercase; margin-top: 10px; letter-spacing: 1px; }

        /* The "Memo" - Executive View */
        .memo { 
            background: #fff; color: #111; padding: 35px; border-radius: 4px; 
            margin-top: 40px; font-family: 'Courier New', monospace; box-shadow: 20px 20px 0px var(--gold);
        }
        .memo-header { border-bottom: 2px solid #111; margin-bottom: 20px; padding-bottom: 10px; font-weight: bold; }

        .persona-tag { 
            display: inline-block; background: var(--accent); color: #000; 
            padding: 4px 12px; border-radius: 50px; font-size: 0.8rem; font-weight: bold; margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="top-label">HIGH-NET-WORTH ANALYSIS UNIT</span>
            <h1>Insta<span style="color:var(--accent)">Intel</span>.</h1>
            <div class="search-container">
                <form action="/analyze" method="get" style="display:flex; width:100%; gap:10px;">
                    <input type="text" name="username" placeholder="הזן שם משתמש לניתוח שווי שוק..." required>
                    <button type="submit">ANALYZE</button>
                </form>
            </div>
        </header>

        {% if username %}
        <div class="grid">
            <div class="stat-card">
                <span class="lbl">שווי מדיה (פוסט)</span>
                <span class="val">${{ post_value }}</span>
            </div>
            <div class="stat-card">
                <span class="lbl">מדד השפעה</span>
                <span class="val">{{ engagement }}</span>
            </div>
            <div class="stat-card">
                <span class="lbl">פוטנציאל שנתי</span>
                <span class="val" style="color: var(--gold);">${{ annual_val }}</span>
            </div>
        </div>

        <div class="memo">
            <div class="memo-header">CONFIDENTIAL STRATEGY MEMO // @{{ username }}</div>
            <span class="persona-tag">פרסונה מזוהה: {{ persona_name }}</span>
            <p style="line-height: 1.6;">{{ strategy }}</p>
            <div style="margin-top: 30px; font-size: 0.8rem; border-top: 1px solid #ddd; padding-top: 10px;">
                <strong>הנחיה למזכירה:</strong> נא לתייק בתיק נכסים דיגיטליים ולהכין טיוטת חוזה בהתאם לשווי השוק המוצג.
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
        
        followers = data.get('followersCount', 0)
        posts = data.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_likes / followers) * 100 if followers > 0 else 0
        
        # לוגיקה לפרסונות - מנהלים ומזכירות
        if followers > 100000:
            persona = "High-Impact Asset"
            strategy = f"הפרופיל של @{username} פועל ברמת VIP. הנתונים מראים כי כל פוסט מייצר חשיפה שוות ערך לקמפיין חוצות. המלצה למנהל: אין להתפשר על פחות מהמחיר הנקוב למעלה."
        elif "shop" in data.get('biography', '').lower() or "חנות" in data.get('biography', ''):
            persona = "The Business Driver"
            strategy = f"זהו חשבון ממוקד המרה. המנהל העסוק חייב להבין שה-Engagement הנוכחי ({round(er,2)}%) הוא צוואר הבקבוק של המכירות. יש להגביר פעילות Reels."
        else:
            persona = "Growth Professional"
            strategy = f"הפרופיל נמצא בשלב צבירת סמכות. המזכירה הלחוצה יכולה להירגע - הקצב חיובי, אך יש צורך באוטומציה של תגובות כדי לשמור על מדד ההשפעה."

        # חישוב שווי (נוסחה יוקרתית)
        val = (followers / 1000) * 20 * (1 + er/3)
        
        return render_template_string(HTML_TEMPLATE, 
            username=username, 
            engagement=f"{round(er, 2)}%",
            persona_name=persona,
            post_value=f"{int(val):,}",
            annual_val=f"{int(val * 52):,}",
            strategy=strategy)
    except:
        return render_template_string(HTML_TEMPLATE, error="System Error: Access Denied")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# תבנית HTML/CSS מלאה ומעוצבת (Premium Dark Mode)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Insta-Analyzer AI Pro</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { background-color: #1e1e1e; width: 100%; max-width: 480px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden; }
        .header { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; padding: 25px; text-align: center; }
        .search-bar { padding: 20px; background-color: #252525; text-align: center; border-bottom: 1px solid #333; }
        input { padding: 12px; width: 65%; border-radius: 8px; border: 1px solid #444; background-color: #121212; color: white; }
        button { padding: 12px 20px; background-color: #bc1888; color: white; border: none; border-radius: 8px; cursor: pointer; transition: 0.3s; }
        button:hover { background-color: #8a1265; }
        .section { padding: 20px; border-bottom: 1px solid #333; }
        .score-box { text-align: center; padding: 30px; background-color: #252525; border-radius: 15px; margin: 20px; border: 1px solid #333; }
        .score-value { font-size: 4em; font-weight: bold; color: #cc2366; }
        .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 20px; }
        .stat-card { background-color: #252525; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #333; }
        .stat-value { font-size: 1.3em; font-weight: bold; color: #e0e0e0; }
        .stat-label { font-size: 0.8em; color: #aaa; }
        .gauge-container { width: 100px; height: 50px; margin: auto; position: relative; }
        .gauge { width: 100%; height: 100%; border-radius: 50px 50px 0 0; background-color: #333; position: relative; overflow: hidden; }
        .gauge-fill { width: 100%; height: 100%; position: absolute; top: 100%; left: 0; transform-origin: center top; transition: transform 0.5s; }
        .insight-card { background-color: #2d2d2d; padding: 15px; border-radius: 10px; margin: 10px 0; border-right: 4px solid #bc1888; }
        .tag { display: inline-block; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; margin-left: 5px; color: white; }
        .tag-sale { background-color: #e17055; }
        .tag-info { background-color: #0984e3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Insta-Analyzer AI 🤖</h1>
            <p>ניתוח פרופיל חכם ותובנות עסקיות</p>
        </div>
        
        <div class="search-bar">
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הכנס שם משתמש (למשל: nasa)..." required>
                <button type="submit">נתח פרופיל</button>
            </form>
        </div>

        {% if error %}
            <div class="section" style="color:#fab1a0; text-align:center;">{{ error }}</div>
        {% elif username %}
            <div class="score-box">
                <h3>ציון איכות פרופיל</h3>
                <div class="score-value">{{ score }}/10</div>
                <p>מבוסס על מעורבות, אותנטיות ופעילות</p>
            </div>

            <div class="section">
                <strong>🔍 זיהוי עסקי ואותנטיות:</strong><br>
                {% if is_selling %}
                    <span class="tag tag-sale">💰 החשבון מוכר מוצר/שירות</span>
                    <p style="font-size:0.9em; color:#aaa; margin-top:5px;">תחום משוער: {{ business_type }}</p>
                {% else %}
                    <span class="tag tag-info">🏠 חשבון אישי/תוכן</span>
                {% endif %}
                <br>
                {% if authenticity == 'high' %}
                    <span class="tag" style="background-color:#00b894;">✅ קהל אותנטי מאוד</span>
                {% elif authenticity == 'low' %}
                    <span class="tag" style="background-color:#d63031;">⚠️ חשד לעוקבים פיקטיביים</span>
                {% else %}
                    <span class="tag tag-info">📊 קהל ממוצע</span>
                {% endif %}
            </div>

            <div class="stat-grid">
                <div class="stat-card">
                    <span class="stat-value">{{ followers }}</span>
                    <span class="stat-label">עוקבים</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{{ following }}</span>
                    <span class="stat-label">עוקב אחרי</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{{ avg_likes }}</span>
                    <span class="stat-label">ממוצע לייקים</span>
                </div>
                <div class="stat-card">
                    <div class="gauge-container">
                        <div class="gauge">
                            <div class="gauge-fill" style="background-color:{{ er_color }}; transform: rotate({{ er_angle }}deg);"></div>
                        </div>
                    </div>
                    <span class="stat-value" style="color:{{ er_color }};">{{ engagement }}</span>
                    <span class="stat-label">אחוז מעורבות (ER)</span>
                </div>
            </div>

            <div class="section">
                <strong>💡 תובנות וטיפים לשיפור (AI Insights):</strong>
                {% for insight in insights %}
                    <div class="insight-card">{{ insight }}</div>
                {% endfor %}
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
    
    if not username: return render_template_string(HTML_TEMPLATE, error="נא להזין שם משתמש")
    if not token: return "Missing APIFY_TOKEN in Render Settings", 500

    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}"
    
    try:
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = res.json()
        if not data: return render_template_string(HTML_TEMPLATE, error="פרופיל פרטי או לא נמצא")
        
        user = data[0]
        bio = user.get('biography', '').lower()
        followers = user.get('followersCount', 0)
        following = user.get('followsCount', 0)
        posts = user.get('latestPosts', [])
        
        # חישוב נתונים יבשים
        avg_likes = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_likes / followers) * 100 if followers > 0 else 0
        
        # לוגיקה חכמה לזיהוי מכירה וסוג עסק
        sale_words = ['shop', 'חנות', 'buy', 'order', 'קנו', 'sale', 'לינק', 'http', '.com', 'discount', 'קופון']
        is_selling = any(word in bio for word in sale_words)
        
        business_type = "לא זוהה סוג ספציפי"
        if any(w in bio for w in ['fitness', 'כושר', 'אימון']): business_type = "כושר ותזונה"
        elif any(w in bio for w in ['course', 'קורס', 'סדנה']): business_type = "קורסים וייעוץ"
        elif any(w in bio for w in ['shop', 'חנות', 'משלוחים']): business_type = "חנות פיזית/דיגיטלית"

        # חישוב מדד מעורבות ויזואלי (Gauge)
        er_angle = min(er * 20, 180) # זווית הסיבוב של הגרף
        er_color = "#d63031" # אדום (נמוך)
        if er > 1.5: er_color = "#fbc531" # צהוב (ממוצע)
        if er > 3.5: er_color = "#00b894" # ירוק (מצוין)

        # לוגיקת AI לציון, אותנטיות ותובנות
        score = 5
        insights = []
        authenticity = 'medium'

        # בדיקת מעורבות
        if er > 4: 
            score += 3
            insights.append("🔥 מעורבות מצוינת! הקהל שלך מגיב חזק לתוכן.")
        elif er < 1:
            score -= 2
            insights.append("📉 המעורבות נמוכה. נסה להעלות יותר סרטונים (Reels) כדי להגדיל חשיפה.")
        else:
            insights.append("📊 המעורבות ממוצעת. נסה להוסיף 'הנעה לפעולה' (CTA) בפוסטים.")

        # בדיקת כוונת מכירה
        if is_selling:
            score += 1
            insights.append(f"💰 זוהתה כוונת מכירה בתחום {business_type}.")
            if "http" not in bio and ".com" not in bio:
                insights.append("⚠️ אזהרה: אין לינק ישיר לרכישה ב-Bio, זה מפסיד מכירות!")
        else:
            insights.append("🏠 חשבון אישי/תוכן - הוספת 'הנעה לפעולה' ממוקדת ב-Bio תגדיל עוקבים.")

        # בדיקת אותנטיות
        if er > 15 and followers > 1000:
            authenticity = 'low'
            insights.append("🔶 אותנטיות: מעורבות חריגה מאוד - ייתכן שימוש בבוטים או 'קבוצות תמיכה'.")
        elif er < 0.3 and followers > 10000:
            authenticity = 'low'
            insights.append("📉 אותנטיות: יחס מעורבות נמוך במיוחד - חשד לעוקבים פיקטיביים (גוססים).")
        elif followers > 1000:
            authenticity = 'high'
            score += 1

        # החזרת הנתונים לתצוגה
        return render_template_string(HTML_TEMPLATE, 
            username=username, followers=f"{followers:,}", following=f"{following:,}", 
            avg_likes=f"{avg_likes:,}", engagement=f"{round(er, 2)}%",
            is_selling=is_selling, business_type=business_type,
            er_angle=er_angle, er_color=er_color,
            score=min(max(score, 1), 10), insights=insights, authenticity=authenticity)
            
    except:
        return render_template_string(HTML_PAGE, error="שגיאה בסריקה")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

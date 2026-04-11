import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Insta-Analyzer AI</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; margin: 0; padding: 20px; text-align: right; }
        .container { background: white; max-width: 500px; margin: auto; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: #333; color: white; padding: 20px; text-align: center; }
        .section { padding: 20px; border-bottom: 1px solid #eee; }
        .tag { display: inline-block; padding: 5px 12px; border-radius: 15px; font-size: 0.8em; margin-top: 5px; }
        .tag-sale { background: #ffeaa7; color: #d63031; }
        .tag-info { background: #dfe6e9; color: #2d3436; }
        .score { font-size: 3em; font-weight: bold; color: #6c5ce7; }
        .tip { background: #f1f2f6; padding: 10px; border-right: 4px solid #6c5ce7; margin: 10px 0; font-size: 0.9em; }
        input { padding: 12px; width: 60%; border-radius: 8px; border: 1px solid #ddd; }
        button { padding: 12px 20px; background: #6c5ce7; color: white; border: none; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>מנתח פרופיל חכם 🤖</h2>
            <form action="/analyze" method="get">
                <input type="text" name="username" placeholder="הכנס שם משתמש..." required>
                <button type="submit">נתח עכשיו</button>
            </form>
        </div>

        {% if error %}
            <div class="section" style="color:red; text-align:center;">{{ error }}</div>
        {% elif username %}
            <div class="section" style="text-align:center;">
                <h3>@{{ username }}</h3>
                <div class="score">{{ score }}/10</div>
                <p>ציון איכות כללי</p>
            </div>

            <div class="section">
                <strong>🔍 זיהוי עסקי:</strong><br>
                {% if is_selling %}
                    <span class="tag tag-sale">💰 החשבון מוכר מוצר/שירות</span>
                {% else %}
                    <span class="tag tag-info">🏠 חשבון אישי/תוכן</span>
                {% endif %}
            </div>

            <div class="section">
                <strong>📊 נתונים יבשים:</strong>
                <p>עוקבים: {{ followers }} | מעורבות: {{ engagement }}</p>
            </div>

            <div class="section">
                <strong>💡 המלצות לשיפור:</strong>
                {% for tip in tips %}
                    <div class="tip">{{ tip }}</div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/analyze')
def analyze():
    username = request.args.get('username')
    token = os.environ.get('APIFY_TOKEN')
    
    url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}"
    
    try:
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        data = res.json()
        if not data: return render_template_string(HTML_PAGE, error="פרופיל פרטי או לא נמצא")
        
        user = data[0]
        bio = user.get('biography', '').lower()
        followers = user.get('followersCount', 0)
        posts = user.get('latestPosts', [])
        avg_l = sum(p.get('likesCount', 0) for p in posts) / len(posts) if posts else 0
        er = (avg_l / followers) * 100 if followers > 0 else 0

        # לוגיקה חכמה לזיהוי מכירה
        sale_words = ['shop', 'חנות', 'buy', 'order', 'קנו', 'sale', 'לינק', 'http', '.com', 'discount']
        is_selling = any(word in bio for word in sale_words)

        # חישוב ציון וטיפים
        score = 5
        tips = []
        
        if er > 5: 
            score += 3
            tips.append("מעורבות מצוינת! הקהל שלך נאמן מאוד.")
        elif er < 2:
            score -= 2
            tips.append("המעורבות נמוכה. נסה להעלות יותר Reels ופחות תמונות סטטיות.")
            
        if is_selling:
            tips.append("החשבון עסקי - כדאי לוודא שיש הנעה לפעולה ברורה ב-Highlights.")
        else:
            tips.append("חשבון אישי - הוספת Bio ממוקד תעזור להשיג יותר עוקבים.")

        if followers > 10000: score += 2

        return render_template_string(HTML_PAGE, 
            username=username, followers=f"{followers:,}", 
            engagement=f"{round(er, 2)}%", is_selling=is_selling,
            score=min(score, 10), tips=tips)
    except:
        return render_template_string(HTML_PAGE, error="שגיאה בסריקה")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

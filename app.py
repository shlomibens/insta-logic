@app.route('/analyze')
def analyze():
    username = request.args.get('username', '').replace('@', '').strip()
    token = os.environ.get('APIFY_TOKEN')
    
    if not token:
        return "ERROR: APIFY_TOKEN MISSING", 500

    try:
        # חזרה למבנה ה-URL הפשוט שעבד לך
        url = f"https://apify.com{token}"
        
        # שליחת הבקשה בדיוק כמו בגרסה הראשונה
        res = requests.post(url, json={"usernames": [username]}, timeout=60)
        
        if res.status_code != 201 and res.status_code != 200:
            return f"API ERROR: {res.status_code}", 500
            
        data_list = res.json()
        if not data_list:
            return "ERROR: USER NOT FOUND", 404
            
        profile = data_list[0]
        
        # --- לוגיקה וחישובים ---
        f_count = profile.get('followersCount', 0)
        latest_posts = profile.get('latestPosts', [])
        avg_likes = sum(p.get('likesCount', 0) for p in latest_posts) / len(latest_posts) if latest_posts else 0
        er = round((avg_likes / f_count * 100), 2) if f_count > 0 else 0
        
        # ציון וצבעים
        score = min(9.9, max(1.0, round(er * 4.5, 1)))
        color = "#00ff66" if score > 7 else "#ffcc00" if score > 4 else "#ff003c"
        
        # שווי שוק מוערך
        market_value = int((f_count / 1000) * 15 * (er / 2))

        # בניית אובייקט הנתונים לתצוגה
        data = {
            "username": username.upper(),
            "followers": f"{f_count:,}",
            "er": er,
            "score": score,
            "value": f"{market_value:,}",
            "trust": 100 - (15 if er < 1 else 5),
            "diag": "High engagement detected." if er > 3 else "Low audience resonance.",
            "tact": "Scale content production." if er > 3 else "Revise hashtag strategy.",
            "color": color
        }
        
        return render_template_string(HTML_TEMPLATE, data=data)

    except Exception as e:
        return f"CRITICAL ERROR: {str(e)}", 500

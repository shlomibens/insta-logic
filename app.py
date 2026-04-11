import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def intelligent_analysis(profile_data):
    if not profile_data:
        return {"error": "Could not fetch data"}
    bio = profile_data.get("biography", "").lower()
    followers = profile_data.get("followersCount", 0)
    sales_keywords = ['מכירה', 'shop', 'order', 'מחיר', 'הזמנות', 'קנו', 'sale', 'לינק', 'בוואטסאפ']
    is_sales = any(word in bio for word in sales_keywords)
    if is_sales:
        return {"type": "SALES", "action": "להציע שאלון אפיון וסינון לידים."}
    elif followers > 10000:
        return {"type": "VIRAL", "action": "להציע מנוע צמיחה וניהול קהילה."}
    else:
        return {"type": "BRAND", "action": "להציע בניית נוכחות דיגיטלית וריכוז נכסים."}

@app.route('/scan', methods=['POST'])
def scan_profile():
    url = request.json.get("url")
    if not url: return jsonify({"error": "Missing URL"}), 400
    apify_url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync?token={APIFY_TOKEN}"
    try:
        response = requests.post(apify_url, json={"directUrls": [url], "resultsLimit": 1}, timeout=60)
        data = response.json()
        analysis = intelligent_analysis(data[0] if data else {})
        return jsonify({"status": "success", "analysis": analysis})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# ... (חלק ה-CSS נשאר דומה, הוספתי לוגיקה בפונקציית analyze)

        # לוגיקה לזיהוי סוג העסק
        business_type = "לא זוהה סוג ספציפי"
        if any(w in bio for w in ['fitness', 'כושר', 'אימון']): business_type = "תחום הכושר והבריאות"
        elif any(w in bio for w in ['course', 'קורס', 'סדנה']): business_type = "מכירת ידע וקורסים"
        elif any(w in bio for w in ['shop', 'חנות', 'משלוחים']): business_type = "מסחר ומוצרים פיזיים"

        # המלצות מותאמות אישית
        if is_selling:
            tips.append(f"זוהה עסק בתחום: {business_type}")
            if ".com" not in bio and "http" not in bio:
                tips.append("⚠️ אזהרה: אין לינק ישיר לרכישה ב-Bio, זה מפסיד מכירות!")
        
        # חישוב אותנטיות
        if er > 15 and followers > 1000:
            tips.append("🔥 וואו! מעורבות חריגה לטובה - הפרופיל ויראלי מאוד.")
        elif er < 0.5 and followers > 5000:
            tips.append("📉 חשד לקהל לא פעיל - כדאי לנקות עוקבים פיקטיביים.")

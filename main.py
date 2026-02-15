import requests
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- [إعدادات الإمبراطورية] ---
MY_COUPON_CODE = "MSHL1" 
MY_AFFILIATE_LINK = "https://www.noon.com/saudi-ar" 
SENDER_EMAIL = "oedn305@gmail.com"
MAIL_PASS = "nfripukmtxqwlxhl"
TARGET_BLOG = "oedn305.Nnnon@blogger.com"

# قائمة مفاتيح (تقدر تضيف أكثر من واحد هنا للتدوير)
API_KEYS = ["AIzaSyBCqHSQLQFTLCUsTc5QTcfKSu-C2k5vL5U"] 

# --- [قائمة المنتجات] ---
OFFERS = [
    {"name": "iPhone 16 Pro 256GB", "price": "4049 SAR", "old": "4,699 SAR", "features": "كاميرا احترافية، أداء جبار، شاشة ProMotion"},
    {"name": "MacBook Air M4", "price": "4,199 SAR", "old": "5,899 SAR", "features": "نحيف جداً، بطارية تدوم طويلاً، معالج M4 الجديد"},
    {"name": "Dyson Airwrap", "price": "1499 SAR", "old": "2443 SAR", "features": "تصفيف احترافي، حماية من الحرارة، نتائج صالون"},
    {"name": "Samsung 75\" TV", "price": "1,999 SAR", "old": "3,999 SAR", "features": "دقة 4K، شاشة عملاقة، ألوان كريستالية"},
    {"name": "AirPods 4", "price": "469 SAR", "old": "599 SAR", "features": "عزل ضجيج، صوت محيطي، شحن لاسلكي"}
]

def generate_local_desc(item):
    """نظام توليد وصف محلي لضمان الخدمة إذا توقف الـ API"""
    phrases = [
        f"أقوى العروض وصلت! احصل على {item['name']} بمواصفات خيالية تشمل {item['features']}.",
        f"لا تفوت فرصة التوفير مع متجر تم، {item['name']} متوفر الآن بسعر محروق.",
        f"إذا كنت تبحث عن الجودة والسعر، {item['name']} هو خيارك الأفضل مع ضمان نون."
    ]
    return random.choice(phrases)

def run_noon_bot():
    try:
        item = random.choice(OFFERS)
        print(f"🚀 جاري تشغيل الخدمة لمنتج: {item['name']}")
        
        full_text = generate_local_desc(item) # الوصف الأساسي جاهز فوراً
        
        # محاولة تحديث الوصف بذكاء اصطناعي (اختياري)
        for key in API_KEYS:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                prompt = f"اكتب مقال تسويقي قصير لـ {item['name']} كود خصم {MY_COUPON_CODE}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
                data = res.json()
                if 'candidates' in data:
                    full_text = data['candidates'][0]['content']['parts'][0]['text']
                    print("✨ تم تحديث المحتوى عبر السيرفر.")
                    break
            except:
                continue

        # تصميم الفولاذي (HTML)
        html_body = f"""
        <div dir="rtl" style="text-align: right; font-family: sans-serif; border: 3px solid #feee00; padding: 25px; border-radius: 15px; background: #fff;">
            <h2 style="color: #d32f2f;">🔥 متجر تم يقدم: {item['name']}</h2>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p style="font-size: 20px;">السعر الحصري: <span style="color: #2e7d32; font-weight: bold;">{item['price']}</span></p>
                <p style="color: #666;">السعر قبل الخصم: <strike>{item['old']}</strike></p>
            </div>
            
            <div style="background: #000; color: #feee00; padding: 20px; text-align: center; border-radius: 10px;">
                <p style="margin: 0; font-size: 18px;">كود الخصم الإضافي لمتجر نون:</p>
                <h1 style="font-size: 60px; margin: 10px 0;">{MY_COUPON_CODE}</h1>
                <a href="{MY_AFFILIATE_LINK}" style="display: inline-block; background: #feee00; color: #000; padding: 12px 30px; text-decoration: none; font-weight: bold; border-radius: 5px;">تسوق الآن وفعل الخصم</a>
            </div>

            <div style="margin-top: 20px; line-height: 1.8; color: #333;">
                <h3>لماذا تشتري هذا المنتج؟</h3>
                <p>{full_text}</p>
                <ul><li>مواصفات حصرية: {item['features']}</li></ul>
            </div>
        </div>
        """

        msg = MIMEMultipart()
        msg['Subject'] = f"🔥 عرض متاح الآن: {item['name']} (كود خصم نون: {MY_COUPON_CODE})"
        msg['From'] = f"متجر تم <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح. الخدمة مستمرة...")

    except Exception as e:
        print(f"❌ عطل طارئ: {e}")

if __name__ == "__main__":
    run_noon_bot()

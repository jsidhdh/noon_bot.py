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
API_KEY = "AIzaSyBCqHSQLQFTLCUsTc5QTcfKSu-C2k5vL5U"

# --- [قائمة المنتجات] ---
OFFERS = [
    {"name": "iPhone 16 Pro 256GB - Desert Titanium", "price": "4049 AED", "old": "4,699 AED"},
    {"name": "Apple MacBook Air 13” M4 MW123", "price": "4,199 SAR", "old": "5,899 SAR"},
    {"name": "Dyson Airwrap Multi-Styler", "price": "1499 SAR", "old": "2443 SAR"},
    {"name": "Samsung 75\" Crystal UHD Smart TV", "price": "1,999 AED", "old": "3,999 AED"},
    {"name": "Sony DualSense Wireless Controller PS5", "price": "209 SAR", "old": "484 SAR"},
    {"name": "Calvin Klein Eternity Moment EDP 100ml", "price": "83 SAR", "old": "405 SAR"},
    {"name": "Apple AirPods 4", "price": "469 SAR", "old": "599 SAR"}
]

def run_noon_bot():
    try:
        item = random.choice(OFFERS)
        print(f"📦 جاري تجهيز عرض لـ: {item['name']}")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        prompt = (f"اكتب مقال تسويقي عربي قصير ومثير لمنتج {item['name']} بسعر {item['price']}. "
                  f"ركز على كود الخصم {MY_COUPON_CODE}. استخدم HTML للتنسيق.")
        
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        full_text = res.json()['candidates'][0]['content']['parts'][0]['text']
        
        html_body = f"""
        <div dir="rtl" style="text-align: right; font-family: sans-serif; border: 2px solid #feee00; padding: 20px;">
            <h2 style="color: #d32f2f;">🔥 عرض حصري: {item['name']}</h2>
            <p>وفر الآن واحصل عليه بسعر <b>{item['price']}</b> بدلاً من <strike>{item['old']}</strike></p>
            <div style="background: #fff9c4; padding: 15px; border: 1px dashed #000; text-align: center;">
                <p>كود الخصم الإضافي:</p>
                <h1 style="font-size: 40px;">{MY_COUPON_CODE}</h1>
                <a href="{MY_AFFILIATE_LINK}" style="background: #000; color: #feee00; padding: 10px 20px; text-decoration: none; font-weight: bold;">تفعيل الخصم الآن</a>
            </div>
            <div style="margin-top: 20px;">{full_text}</div>
        </div>
        """

        msg = MIMEMultipart()
        msg['Subject'] = f"🔥 عرض مجنون على {item['name']} - كود {MY_COUPON_CODE}"
        msg['From'] = f"Noon VIP <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.send_mail(SENDER_EMAIL, TARGET_BLOG, msg.as_string())
        
        print("✅ تم النشر في المدونة!")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_noon_bot()

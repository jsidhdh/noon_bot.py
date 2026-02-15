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
        # اختيار منتج عشوائي
        item = random.choice(OFFERS)
        print(f"📦 جاري العمل على منتج: {item['name']}")
        
        # طلب كتابة وصف من جيميني
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        prompt = (f"اكتب مقال تسويقي عربي قصير ومثير لمنتج {item['name']} بسعر {item['price']}. "
                  f"ركز على أن هذا السعر متاح فقط عند استخدام كود الخصم {MY_COUPON_CODE}. "
                  f"استخدم HTML للتنسيق مثل <b> و <p>.")
        
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        full_text = res.json()['candidates'][0]['content']['parts'][0]['text']
        
        # تصميم البوست (HTML)
        html_body = f"""
        <div dir="rtl" style="text-align: right; font-family: sans-serif; border: 2px solid #feee00; padding: 20px; border-radius: 10px;">
            <h2 style="color: #d32f2f;">🔥 عرض متجر تم الحصري: {item['name']}</h2>
            <p style="font-size: 18px;">احصل عليه الآن بسعر <b>{item['price']}</b> فقط بدلاً من <strike>{item['old']}</strike></p>
            <div style="background: #fff9c4; padding: 20px; border: 20px solid #feee00; text-align: center; margin: 15px 0;">
                <p style="font-weight: bold; font-size: 20px;">كود خصم نون الإضافي:</p>
                <h1 style="font-size: 50px; color: #000; margin: 10px 0;">{MY_COUPON_CODE}</h1>
                <a href="{MY_AFFILIATE_LINK}" style="background: #000; color: #feee00; padding: 12px 25px; text-decoration: none; font-weight: bold; font-size: 18px; border-radius: 5px; display: inline-block;">اضغط هنا لتفعيل الخصم</a>
            </div>
            <div style="line-height: 1.8; color: #444;">{full_text}</div>
            <p style="color: #888; font-size: 12px; margin-top: 20px;">* العرض متاح لفترة محدودة عبر متجر تم.</p>
        </div>
        """

        # إرسال الرسالة إلى بلوجر
        msg = MIMEMultipart()
        msg['Subject'] = f"🔥 عرض حصري من متجر تم: {item['name']} - كود {MY_COUPON_CODE}"
        msg['From'] = f"Noon VIP Offers <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح لمنتج {item['name']}")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_noon_bot()

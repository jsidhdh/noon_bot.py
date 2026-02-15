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
        print(f"📦 جاري العمل على منتج: {item['name']}")
        
        # وصف احتياطي (لو فشل الذكاء الاصطناعي)
        full_text = f"فرصة حصرية للحصول على {item['name']} بأفضل سعر من متجر نون. منتج أصلي ومضمون مع شحن سريع."
        
        # محاولة طلب الوصف من Gemini (مع حماية ضد الأخطاء)
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            prompt = (f"اكتب مقال تسويقي عربي قصير ومثير لمنتج {item['name']} بسعر {item['price']}. "
                      f"ركز على أن هذا السعر متاح فقط عند استخدام كود الخصم {MY_COUPON_CODE}. استخدم HTML.")
            
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            data = res.json()
            
            # التأكد من أن الرد يحتوي على النتائج المطلوبة
            if 'candidates' in data and len(data['candidates']) > 0:
                full_text = data['candidates'][0]['content']['parts'][0]['text']
                print("✨ تم توليد الوصف بنجاح.")
            else:
                print("⚠️ الذكاء الاصطناعي لم يستجب بشكل صحيح، نستخدم الوصف الاحتياطي.")
        except:
            print("⚠️ فشل الاتصال بالذكاء الاصطناعي، نستخدم الوصف الاحتياطي.")

        # تصميم الإيميل (HTML)
        html_body = f"""
        <div dir="rtl" style="text-align: right; font-family: Arial, sans-serif; border: 2px solid #feee00; padding: 25px; border-radius: 15px;">
            <h2 style="color: #d32f2f; border-bottom: 2px solid #feee00; padding-bottom: 10px;">🔥 عرض متجر تم الحصري: {item['name']}</h2>
            <p style="font-size: 1.1em;">احصل عليه الآن بسعر <b>{item['price']}</b> فقط بدلاً من <strike>{item['old']}</strike></p>
            
            <div style="background: #fff9c4; padding: 25px; border: 2px dashed #000; text-align: center; margin: 20px 0;">
                <p style="font-weight: bold; font-size: 1.2em;">استخدم كود خصم نون الذهبي للحصول على التوفير:</p>
                <h1 style="font-size: 55px; color: #000; margin: 10px 0;">{MY_COUPON_CODE}</h1>
                <a href="{MY_AFFILIATE_LINK}" style="background: #000; color: #feee00; padding: 15px 35px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; font-size: 1.1em;">تفعيل الخصم في نون الآن</a>
            </div>

            <div style="line-height: 1.8; color: #333; font-size: 1.05em;">{full_text}</div>
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #888; font-size: 0.9em; text-align: center;">* ملاحظة: العرض متوفر عبر متجر تم السعودية لفترة محدودة.</p>
        </div>
        """

        # إرسال الرسالة
        msg = MIMEMultipart()
        msg['Subject'] = f"🔥 عرض حصري من متجر تم: {item['name']} - كود {MY_COUPON_CODE}"
        msg['From'] = f"Noon VIP Offers <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح! ({item['name']})")

    except Exception as e:
        print(f"❌ خطأ فادح غير متوقع: {e}")

if __name__ == "__main__":
    run_noon_bot()

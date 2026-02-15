import time
import random
import schedule
import requests
# أي import آخر أعطيتك إياه ضيفه هنا
import requests
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- [إعدادات الإمبراطورية] ---
MY_COUPON_CODE = "MSHL1" # كودك الذهبي
MY_AFFILIATE_LINK = "https://www.noon.com/saudi-ar" # رابط الأفلييت
SENDER_EMAIL = "oedn305@gmail.com"
MAIL_PASS = "nfripukmtxqwlxhl"
TARGET_BLOG = "oedn305.Nnnon@blogger.com"
API_KEY = "AIzaSyBCqHSQLQFTLCUsTc5QTcfKSu-C2k5vL5U"

# --- [قائمة المنتجات الشاملة] ---
OFFERS = [
    {"name": "iPhone 16 Pro 256GB - Desert Titanium", "price": "4049 AED", "old": "4,699 AED", "cat": "جوالات"},
    {"name": "Apple MacBook Air 13” M4 MW123", "price": "4,199 SAR", "old": "5,899 SAR", "cat": "لابتوبات"},
    {"name": "Dyson Airwrap Multi-Styler", "price": "1499 SAR", "old": "2443 SAR", "cat": "جمال"},
    {"name": "Samsung 75\" Crystal UHD Smart TV", "price": "1,999 AED", "old": "3,999 AED", "cat": "شاشات"},
    {"name": "Sony DualSense Wireless Controller PS5", "price": "209 SAR", "old": "484 SAR", "cat": "ألعاب"},
    {"name": "Calvin Klein Eternity Moment EDP 100ml", "price": "83 SAR", "old": "405 SAR", "cat": "عطور"},
    {"name": "Roberto Cavalli Florence EDP 75ml", "price": "94 AED", "old": "395 AED", "cat": "عطور"},
    {"name": "Kerastase Genesis Bain Shampoo", "price": "99 AED", "old": "152 AED", "cat": "عناية بالشعر"},
    {"name": "100% Cotton Bath Mat", "price": "1 AED", "old": "16 AED", "cat": "منزل"},
    {"name": "Lightweight Summer Blanket", "price": "1 AED", "old": "57 AED", "cat": "منزل"},
    {"name": "Hikvision D1 Dashcam", "price": "69 SAR", "old": "139 SAR", "cat": "سيارات"},
    {"name": "Ninebot E2 D E Foldable Scooter", "price": "729 AED", "old": "1,299 AED", "cat": "سكوترات"},
    {"name": "Apple AirPods 4", "price": "469 SAR", "old": "599 SAR", "cat": "سماعات"}
]

def run_noon_bot():
    try:
        item = random.choice(OFFERS)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        # برومبت السيو الاحترافي (SEO & Conversion)
        prompt = (
            f"Write a viral, SEO-optimized shopping guide in Arabic for '{item['name']}'. "
            f"Title must be catchy with 'خصم حصرى' and price. "
            f"Focus on keywords: عروض نون، كود خصم نون السعودية، تخفيضات نون الإمارات، {item['name']}. "
            f"Include: 1. Why this product is a life-changer. 2. Huge discount breakdown. "
            f"3. Direct instruction that price {item['price']} is ONLY for those who use code '{MY_COUPON_CODE}'. "
            f"Use HTML (<h2>, <p>, <b>, <ul>, <li>). Professional and persuasive marketing tone."
        )
        
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        data = res.json()

        if 'candidates' in data:
            full_text = data['candidates'][0]['content']['parts'][0]['text']
            lines = full_text.strip().split('\n')
            subject = lines[0].replace("#", "").strip()
            body = "<br>".join(lines[1:])
        else:
            subject = f"عرض مجنون على {item['name']} - استخدم كود {MY_COUPON_CODE}"
            body = f"<p>وفر الكثير الآن على {item['name']} حصرياً في نون!</p>"

        msg = MIMEMultipart()
        msg['Subject'] = f"🔥 {subject}"
        msg['From'] = f"Noon VIP Offers <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG

        # تصميم الواجهة الاحترافية (Copy & Redirect)
        html = # تصميم "بسيط جداً" لضمان التطابق والتنسيق في أي قالب
        html = f"""
        <div dir="rtl" style="text-align: right; font-family: sans-serif;">
            
            <p style="font-size: 1.2em; color: #333;">
                أهلاً بكم في <b>متجر تم</b>. نقدم لكم اليوم عرضاً حصرياً من متجر نون:
            </p>

            <h2 style="color: #d32f2f;">{item['name']}</h2>
            
            <div style="background: #f0f0f0; padding: 15px; border-right: 5px solid #feee00; margin: 20px 0;">
                <p>السعر الحالي: <b>{item['price']}</b></p>
                <p>السعر قبل الخصم: <strike>{item['old']}</strike></p>
            </div>

            <div style="line-height: 1.8;">
                {body_content}
            </div>

            <hr>

            <div style="text-align: center; background: #fff9c4; padding: 20px; border: 2px dashed #000;">
                <p style="font-weight: bold;">استخدم كود الخصم المعتمد في متجر نون للحصول على التوفير:</p>
                <h1 style="font-size: 45px; color: #000; margin: 10px 0;">{MY_COUPON_CODE}</h1>
                <a href="{MY_AFFILIATE_LINK}" style="display: inline-block; background: #000; color: #feee00; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 18px;">
                    اضغط هنا لتفعيل الخصم في متجر نون
                </a>
            </div>

            <p style="margin-top: 20px; font-size: 0.9em; color: #666;">
                * ملاحظة: هذا العرض متوفر لفترة محدودة عبر متجر تم السعودية.
            </p>
        </div>
        """
# --- هذا آخر شيء في الملف ---
def run_safe_publishing():
    # هنا ينادي البوت الدوال اللي فوق
    print("بدأ النشر...")

# مواعيد النشر
schedule.every().day.at("09:00").do(run_safe_publishing)
schedule.every().day.at("21:00").do(run_safe_publishing)

while True:
    schedule.run_pending()
    time.sleep(60)

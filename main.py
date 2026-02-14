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
        html = f"""
        <div style="direction:rtl; font-family:Arial, sans-serif; border:2px solid #feee00; padding:0; background:#fff; max-width:700px; margin:auto;">
            <div style="background:#feee00; color:#000; padding:15px; text-align:center; font-size:1.3em; font-weight:bold;">
                تنبيه: الخصم يتفعل فقط عند استخدام كود: {MY_COUPON_CODE}
            </div>
            
            <div style="padding:20px;">
                <h1 style="color:#111; text-align:center; font-size:1.8em;">{subject}</h1>
                
                <div style="background:#000; color:#fff; padding:30px; border-radius:15px; text-align:center; margin:25px 0; border:4px solid #feee00;">
                    <p style="margin:0; font-size:1.2em; color:#feee00;">سعر العرض المباشر</p>
                    <h2 style="font-size:3em; margin:10px 0;">{item['price']}</h2>
                    <p style="text-decoration:line-through; color:#888; font-size:1.2em;">السعر الأصلي: {item['old']}</p>
                    
                    <div style="margin-top:20px; padding:15px; background:#222; border:2px dashed #feee00;">
                        <p style="margin:0; font-size:1em; color:#fff;">انسخ كود الخصم الآن:</p>
                        <div id="coupon" style="font-size:3.5em; font-weight:bold; color:#feee00; letter-spacing:5px;">{MY_COUPON_CODE}</div>
                    </div>
                </div>

                <div style="font-size:1.2em; line-height:1.8; color:#333; text-align:right;">
                    {body}
                </div>

                <div style="text-align:center; margin-top:40px; padding:30px; background:#f0f0f0; border-radius:15px;">
                    <h3 style="margin-bottom:20px;">جاهز للتسوق بأقل سعر؟</h3>
                    <button onclick="copyAndRedirect()" style="background:#000; color:#feee00; padding:25px 60px; border:none; font-weight:bold; font-size:1.8em; border-radius:50px; cursor:pointer; border-bottom:6px solid #feee00; width:100%;">
                        انسخ الكود وافتح نون 🚀
                    </button>
                </div>
            </div>
        </div>

        <script>
        function copyAndRedirect() {{
            const el = document.createElement('textarea');
            el.value = '{MY_COUPON_CODE}';
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            
            alert('✅ تم نسخ كود الخصم: {MY_COUPON_CODE}\\n\\nسيتم تحويلك الآن للمتجر، قم بلصق الكود عند الدفع للحصول على الخصم.');
            window.location.href = '{MY_AFFILIATE_LINK}';
        }}
        </script>
        """
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.sendmail(SENDER_EMAIL, [TARGET_BLOG], msg.as_string())
        print(f"✅ تم النشر بنجاح: {item['name']}")

    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_noon_bot()

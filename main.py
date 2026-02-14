import requests
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- الإعدادات الثابتة ---
MY_COUPON_CODE = "MSHL1"
MY_AFFILIATE_LINK = "https://www.noon.com/saudi-ar"

OFFERS = [
    {"name": "iPhone 16 Pro 256GB", "price": "4049 AED", "old": "4,699 AED", "cat": "Mobiles"},
    {"name": "Dyson Airwrap Multi-Styler", "price": "1499 SAR", "old": "2443 SAR", "cat": "Beauty Tech"},
    {"name": "Apple MacBook Air 13” M4", "price": "3,049 AED", "old": "5,009 AED", "cat": "Laptops"},
    {"name": "Samsung 75\" Crystal UHD TV", "price": "1,999 AED", "old": "3,999 AED", "cat": "TVs"},
    {"name": "Roberto Cavalli Florence EDP", "price": "94 AED", "old": "395 AED", "cat": "Perfumes"},
    {"name": "100% Cotton Bath Mat", "price": "1 AED", "old": "16 AED", "cat": "Home"}
]

API_KEY = "AIzaSyBCqHSQLQFTLCUsTc5QTcfKSu-C2k5vL5U"
MAIL_PASS = "nfripukmtxqwlxhl"
SENDER_EMAIL = "oedn305@gmail.com"
TARGET_BLOG = "oedn305.Nnnon@blogger.com"

def run_noon_bot():
    try:
        item = random.choice(OFFERS)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        prompt = (
            f"Write a professional shopping review for '{item['name']}'. "
            f"Stress that the price {item['price']} is ONLY for those who use code '{MY_COUPON_CODE}'. "
            "Use HTML (<h2>, <p>, <b>). The first line must be the TITLE only."
        )
        
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        data = res.json()

        if 'candidates' in data:
            full_text = data['candidates'][0]['content']['parts'][0]['text']
            lines = full_text.strip().split('\n')
            subject = lines[0].replace("#", "").strip()
            body = "<br>".join(lines[1:])
        else:
            subject = f"Special Offer: {item['name']}"
            body = f"<p>Use code {MY_COUPON_CODE} at Noon!</p>"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = f"Noon VIP <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG

        # --- التصميم الجديد مع خاصية النسخ والتحويل الإجباري ---
        html = f"""
        <div style="direction:ltr; font-family:Arial; padding:20px; border:3px solid #feee00; background:#fff;">
            
            <div style="background:#000; color:#fff; padding:25px; border-radius:15px; text-align:center; margin-bottom:25px;">
                <p style="margin:0; font-size:1.2em; color:#feee00;">VIP DISCOUNT PRICE</p>
                <h2 style="font-size:2.5em; margin:10px 0;">{item['price']}</h2>
                <p style="text-decoration:line-through; color:#888;">Was: {item['old']}</p>
            </div>

            <div style="font-size:1.1em; line-height:1.8;">{body}</div>

            <div style="text-align:center; margin-top:40px;">
                <p style="font-weight:bold; color:#d00000;">👇 Click to Copy Code & Open Noon 👇</p>
                
                <button onclick="copyAndGo()" style="background:#feee00; color:#000; padding:25px 50px; border:none; font-weight:bold; font-size:1.8em; border-radius:12px; cursor:pointer; box-shadow: 0 10px 20px rgba(0,0,0,0.1); border-bottom:5px solid #e6c200; width:100%;">
                    ACTIVATE DEAL: {MY_COUPON_CODE}
                </button>

                <script>
                function copyAndGo() {{
                    // إنشاء حقل مخفي لنسخ الكود
                    var tempInput = document.createElement('input');
                    tempInput.value = '{MY_COUPON_CODE}';
                    document.body.appendChild(tempInput);
                    tempInput.select();
                    document.execCommand('copy');
                    document.body.removeChild(tempInput);

                    // رسالة التنبيه الإجبارية للزائر
                    alert('✅ Coupon MSHL1 Copied!\\n\\nPaste it at checkout to get the discount.\\nOpening Noon Store now...');

                    // التوجيه للمتجر
                    window.location.href = '{MY_AFFILIATE_LINK}';
                }}
                </script>
            </div>
            
            <div style="text-align:center; margin-top:20px; color:#777; font-size:0.9em;">
                Code <b>{MY_COUPON_CODE}</b> is ready to be pasted at payment.
            </div>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.sendmail(SENDER_EMAIL, [TARGET_BLOG], msg.as_string())
        print(f"✅ تم النشر بنجاح مع خاصية النسخ والتحويل: {item['name']}")

    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_noon_bot()

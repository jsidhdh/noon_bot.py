import requests
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- الإعدادات الفنية ---
API_KEY = "AIzaSyBCqHSQLQFTLCUsTc5QTcfKSu-C2k5vL5U"
MAIL_PASS = "nfripukmtxqwlxhl"
SENDER_EMAIL = "oedn305@gmail.com"
TARGET_BLOG = "oedn305.Nnnon@blogger.com" 
NOON_LINK = "https://www.noon.com/saudi-ar" 

def run_noon_bot():
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        # تحسين الطلب ليكون أكثر قبولاً لدى السياسات الأمنية
        prompt_text = (
            "Write a helpful 800-word shopping guide and review for a high-quality product available in Saudi Arabia. "
            "Discuss features and benefits in a professional tone. Use HTML tags like <h2> and <p>. "
            "The first line must be the TITLE only."
        )
        
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        res = requests.post(url, json=payload, timeout=45)
        data = res.json()

        # فحص وجود 'candidates' قبل استخدامه لتجنب الـ Error
        if 'candidates' in data and data['candidates']:
            full_text = data['candidates'][0]['content']['parts'][0]['text']
            lines = full_text.strip().split('\n')
            subject = lines[0].replace("#", "").strip()
            body = "<br>".join(lines[1:])
        else:
            # خطة بديلة في حال رفض الذكاء الاصطناعي (عشان ما يطلع لك Error)
            subject = "Exclusive Shopping Guide: Best Deals on Noon Saudi Arabia"
            body = "<h2>Top Picks for You</h2><p>Discover amazing products with great value on Noon today. Our guide helps you choose the best electronics and lifestyle items.</p>"
            print("⚠️ الذكاء الاصطناعي لم يستجب، تم استخدام النص الاحتياطي.")

        img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = f"Noon Market Guide <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG
        
        html = f"""
        <div style='direction:ltr; font-family:Arial; padding:20px; border-top:10px solid #feee00; background:#fff;'>
            <h1 style='color:#222;'>{subject}</h1>
            <img src='{img}' style='width:100%; border-radius:10px;'>
            <div style='font-size:1.1em; line-height:1.8; color:#444;'>{body}</div>
            <div style='text-align:center; background:#feee00; padding:25px; margin-top:20px; border-radius:10px;'>
                <h3 style='margin:0; color:#000;'>Check the offer on Noon</h3>
                <a href='{NOON_LINK}' style='display:inline-block; margin-top:15px; background:#000; color:#fff; padding:15px 35px; text-decoration:none; font-weight:bold; border-radius:5px;'>SHOP ON NOON NOW</a>
            </div>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.sendmail(SENDER_EMAIL, [TARGET_BLOG], msg.as_string())
        print(f"✅ تم النشر بنجاح: {subject}")

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    run_noon_bot()

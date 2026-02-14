import requests
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- إعدادات مدونة نون ---
API_KEY = "AIzaSyBCqHSQLQFTLCUsTc5QTcfKSu-C2k5vL5U"
MAIL_PASS = "nfripukmtxqwlxhl"
SENDER_EMAIL = "oedn305@gmail.com"
TARGET_BLOG = "oedn305.Nnnon@blogger.com" 
NOON_LINK = "https://www.noon.com/saudi-ar" 

def run_noon_bot():
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        prompt = "Write a professional 950-word product review in English for a top item on Noon Saudi Arabia. Use HTML tags. First line is TITLE only."
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        full_text = res.json()['candidates'][0]['content']['parts'][0]['text']
        lines = full_text.strip().split('\n')
        subject = lines[0].replace("#", "").strip()
        body = "<br>".join(lines[1:])
        img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = f"Noon Marketplace <{SENDER_EMAIL}>"
        msg['To'] = TARGET_BLOG
        html = f"<div style='direction:ltr; padding:20px; border-top:10px solid #feee00;'><h1>{subject}</h1><img src='{img}' style='width:100%;'><div>{body}</div><div style='text-align:center; background:#feee00; padding:20px;'><a href='{NOON_LINK}' style='background:#000; color:#fff; padding:15px; text-decoration:none;'>SHOP ON NOON</a></div></div>"
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, MAIL_PASS)
            server.sendmail(SENDER_EMAIL, [TARGET_BLOG], msg.as_string())
        print("✅ Published Successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_noon_bot()

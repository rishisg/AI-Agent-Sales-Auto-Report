import smtplib
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables
load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")

    def send_report(self, report_df, subject, recipient_email, chart_filename=None):
        """Send report via email as CSV attachment and optional chart image"""
        if report_df is None or report_df.empty:
            print("❌ No data available, email not sent.")
            return False

        print(f"📩 Attempting to send report to {recipient_email}...")

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        try:
            # Save report to CSV file
            report_filename = "report.csv"
            report_df.to_csv(report_filename, index=False)

            # Attach CSV file
            with open(report_filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={report_filename}")
                msg.attach(part)

            # Attach chart image if available
            if chart_filename and os.path.exists(chart_filename):
                with open(chart_filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={chart_filename}")
                    msg.attach(part)

            # Send email via SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
            server.quit()

            print("✅ Email sent successfully!")
            return True
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error sending email: {e}")

        return False

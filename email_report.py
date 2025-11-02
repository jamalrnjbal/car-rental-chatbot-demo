"""
Email reporting utility to send conversation summaries to the car rental company.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

COMPANY_EMAIL = "jamalrnjbal@gmail.com"

def send_conversation_report(user_message, bot_response, conversation_history=None):
    """
    Send an email report about a customer query to the company email.

    Args:
        user_message: The latest user message
        bot_response: The bot's response
        conversation_history: Optional list of previous messages
    """
    try:
        # Create email content
        subject = f"Car Rental Chatbot Inquiry - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        # Build the email body
        body = f"""
Car Rental Chatbot Inquiry Report
================================

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Latest Customer Message:
------------------------
{user_message}

Bot Response:
-------------
{bot_response}

"""

        # Add conversation history if available
        if conversation_history and len(conversation_history) > 0:
            body += "\nFull Conversation History:\n"
            body += "=" * 50 + "\n\n"
            for i, msg in enumerate(conversation_history, 1):
                role = "Customer" if msg.get('role') == 'user' else "Bot"
                content = msg.get('content', '')
                body += f"{i}. {role}:\n{content}\n\n"

        body += """
---
This is an automated report from the Car Rental Chatbot system.
"""

        # For now, just print the email content (will configure SMTP later)
        # In production, you would use SMTP to send the email
        print(f"\n{'='*60}")
        print("EMAIL REPORT GENERATED")
        print(f"{'='*60}")
        print(f"To: {COMPANY_EMAIL}")
        print(f"Subject: {subject}")
        print(f"\n{body}")
        print(f"{'='*60}\n")

        return True

    except Exception as e:
        print(f"Error generating email report: {e}")
        return False

def configure_smtp_email(user_message, bot_response, conversation_history=None):
    """
    Alternative function that uses actual SMTP to send emails.
    Requires SMTP credentials in environment variables.

    Environment variables needed:
    - SMTP_SERVER (e.g., smtp.gmail.com)
    - SMTP_PORT (e.g., 587)
    - SMTP_EMAIL (sender email)
    - SMTP_PASSWORD (sender password or app password)
    """
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT', 587)
    smtp_email = os.getenv('SMTP_EMAIL')
    smtp_password = os.getenv('SMTP_PASSWORD')

    if not all([smtp_server, smtp_email, smtp_password]):
        print("SMTP credentials not configured. Email report printed to console instead.")
        return send_conversation_report(user_message, bot_response, conversation_history)

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = COMPANY_EMAIL
        msg['Subject'] = f"Car Rental Chatbot Inquiry - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        # Build body
        body = f"""
Car Rental Chatbot Inquiry Report
================================

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Latest Customer Message:
------------------------
{user_message}

Bot Response:
-------------
{bot_response}

"""

        if conversation_history and len(conversation_history) > 0:
            body += "\nFull Conversation History:\n"
            body += "=" * 50 + "\n\n"
            for i, msg in enumerate(conversation_history, 1):
                role = "Customer" if msg.get('role') == 'user' else "Bot"
                content = msg.get('content', '')
                body += f"{i}. {role}:\n{content}\n\n"

        body += """
---
This is an automated report from the Car Rental Chatbot system.
"""

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)

        print(f"Email report sent successfully to {COMPANY_EMAIL}")
        return True

    except Exception as e:
        print(f"Error sending email via SMTP: {e}")
        # Fallback to console output
        return send_conversation_report(user_message, bot_response, conversation_history)

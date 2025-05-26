import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Import our database module
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.database import DB_PATH

class NotificationManager:
    def __init__(self, email_config=None):
        """Initialize notification manager with optional email configuration."""
        self.email_config = email_config or {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'ganeshagrahari108@gmail.com',
            'sender_password':'2225900004ganesh'
        }
    
    def check_due_reminders(self):
        """Check for due reminders and send notifications."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Get all unsent reminders due today
        cursor.execute('''
        SELECT r.id, u.email, u.name, s.name, s.deadline, s.website_url
        FROM reminders r
        JOIN users u ON r.user_id = u.user_id
        JOIN scholarships s ON r.scholarship_id = s.id
        WHERE r.reminder_date = ? AND r.sent = 0 AND u.email IS NOT NULL
        ''', (today,))
        
        reminders = cursor.fetchall()
        
        for reminder_id, email, name, scholarship_name, deadline, website in reminders:
            if self.send_email_notification(email, name, scholarship_name, deadline, website):
                # Mark reminder as sent
                cursor.execute("UPDATE reminders SET sent = 1 WHERE id = ?", (reminder_id,))
        
        conn.commit()
        conn.close()
        
        return len(reminders)
    
    def send_email_notification(self, recipient_email, recipient_name, scholarship_name, deadline, website_url):
        """Send an email notification about scholarship deadline."""
        try:
            # Create email content
            subject = f"Reminder: {scholarship_name} Deadline Approaching"
            
            message = MIMEMultipart()
            message["From"] = self.email_config['sender_email']
            message["To"] = recipient_email
            message["Subject"] = subject
            
            body = f"""
            Hello {recipient_name},

            This is a reminder that the application deadline for {scholarship_name} is {deadline}.

            Don't miss this opportunity! Visit the official website to apply: {website_url}

            Best regards,
            Scholarship Assistant Bot
            """
            
            message.attach(MIMEText(body, "plain"))
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.sendmail(self.email_config['sender_email'], recipient_email, message.as_string())
            
            return True
        
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False

    def send_sms_notification(self, phone_number, scholarship_name, deadline):
        """Send an SMS notification about scholarship deadline.
        This is a placeholder - you'll need to integrate with an SMS service."""
        # Implement SMS service integration here (e.g., Twilio, AWS SNS)
        print(f"SMS notification to {phone_number} about {scholarship_name} deadline: {deadline}")
        return True

# Usage example:
# notification_mgr = NotificationManager()
# notification_mgr.check_due_reminders()
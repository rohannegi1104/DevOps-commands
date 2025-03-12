import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "rohansingh6814@gmail.com"  
receiver_email = "rohansinghnegi11@gmail.com"  
password = "rohan6814@"  

# Check CPU and RAM usage
cpu_usage = psutil.cpu_percent()
ram_usage = psutil.virtual_memory().percent

# If CPU > 30%  log the alert and send email
if cpu_usage > 30:
    message = f"Warning: CPU usage is too high! Current CPU usage: {cpu_usage}%"
    print(message)

    # Send email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "CPU Usage Alert"
    msg.attach(MIMEText(message, "plain"))
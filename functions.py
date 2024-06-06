from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import random

def send_email(sender, receiver, password, subject, body):
  message = MIMEMultipart("alternative")

  message["Subject"] = subject
  message["From"] = sender
  message["To"] = receiver
  
  message.attach(MIMEText(body, 'plain'))

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())

def generate_id(length):
  code = ""

  numbers = ['1','2','3','4','5','6','7','8','9','0']

  for i in range(length):
    char = random.choice(numbers)

    code += char

  return code

def find_id(users, id):
  for document in list(users.find()):
    if id == document["_id"]:
      return True
    
  return False
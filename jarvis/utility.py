# This module is for the utility functions for features on the Jarvis services background
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "jarvisassistantproto@gmail.com"
password = "jarvis_assistant"

# Sending email to the receiver_email with the message in the body
def sendEmail(receiver_email, message):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context = context)
        server.login(sender_email, password)
        server.sendmail(from_addr = sender_email, to_addrs = receiver_email, msg = message)
    print(f'Message sent to {receiver_email}')



if __name__ == "__main__":
    sendEmail('mariosessa64@gmail.com', "Hi, I am Jarvis!")


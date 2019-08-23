from email.message import EmailMessage
from smtplib import SMTP_SSL


from blog.settings import USER_EMAIL, PASSWORD_EMAIL 

def send_email(mailFrom:str, mailTo:list, mailSubject:str, message:str):
    """
    Tool send email if it succeeds return True else False.
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = mailSubject
    msg['From'] = mailFrom
    msg['To'] = ', '.join(mailTo)
    try:
        serwer = SMTP_SSL('smtp.gmail.com', 465)
        serwer.ehlo()
        serwer.login(user=USER_EMAIL, password=PASSWORD_EMAIL)
        serwer.send_message(msg)
        serwer.quit()
    except:
        return False
    else:
        return True
    
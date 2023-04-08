import smtplib
from config import Config


def send_email(message: str, target_mail: str):
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(Config.mail_user, Config.mail_pass)
    s.sendmail(Config.mail_user, target_mail, message)
    s.quit()

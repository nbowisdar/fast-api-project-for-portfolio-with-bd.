from loguru import logger
import smtplib
from email.message import EmailMessage
import random


class MyEmail:
    def __init__(self, sender: str, password: str, port=465):
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', port)
        smtp.login(sender, password)
        self.sender = sender
        self.__smtp = smtp
        self.port = port

    def disconnect(self):
        self.__smtp.quit()

    def send_code(self, code: str, email_rcv: str):
        msg = EmailMessage()
        msg.set_content(code)
        msg['Subject'] = 'Reset Password'
        msg['From'] = self.sender
        msg['To'] = email_rcv
        self.__smtp.send_message(msg)
        logger.info('Code was send')

    def send_new_password(self, email_rcv: str, new_password: str):
        msg = EmailMessage()
        msg.set_content(new_password)
        msg['Subject'] = 'Your new password'
        msg['From'] = self.sender
        msg['To'] = email_rcv
        self.__smtp.send_message(msg)
        logger.info(f'Sanded new password to {email_rcv}')

    @staticmethod
    def generate_code():
        return str(random.randint(1000, 9999))


# def generate_sender(login: str, mail_recv):
#     pass
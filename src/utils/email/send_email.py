import logging
import smtplib
from email.message import EmailMessage
import random
import asyncio



class MyEmail:
    def __init__(self, sender: str, password: str, port=465):
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', port)
        smtp.login(sender, password)
        self.sender = sender
        self.__smtp = smtp
        self.port = port
        #self.loop = asyncio.get_event_loop()

    def disconnect(self):
        self.__smtp.quit()

    def send_code(self, code: str, email_rcv: str):
        msg = EmailMessage()
        msg.set_content(code)
        msg['Subject'] = 'Reset Password'
        msg['From'] = self.sender
        msg['To'] = email_rcv
        self.__smtp.send_message(msg)
        logging.info('Code was send')

    @staticmethod
    def generate_code():
        return str(random.randint(1000, 9999))


# def generate_sender(login: str, mail_recv):
#     pass
from loguru import logger
import smtplib
from email.message import EmailMessage


class MyEmail:
    def __init__(self, sender: str, password: str, port=465):
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', port)
        smtp.login(sender, password)
        self.sender = sender
        self.__smtp = smtp
        self.port = port

    def disconnect(self):
        self.__smtp.quit()

    async def send_reset_link(self, email_rcv: str, my_msg: str, subject: str):
        msg = EmailMessage()
        msg.set_content(my_msg)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = email_rcv
        self.__smtp.send_message(msg)
        logger.info(f'Sanded new password to {email_rcv}')


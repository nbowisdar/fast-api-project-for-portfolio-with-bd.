from send_email import MyEmail
from loguru import logger

from src.utils.security.jwt.jwt_token import create_access_token
from src.utils.tools.config import MAIL_SENDER, MAIL_PASSWORD
from passwordgenerator import pwgenerator


def send_new_password(mail_recv: str = '380992566619v@gmail.com'):
    mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)
    #new_password = pwgenerator.generate()
    data = {"sub": 'vika',
            'position': 'user'}
    token = create_access_token(data)
    url = f'http://127.0.0.1:8000/user/update_password?token={token}'
    try:
        mail.send_new_password(mail_recv, url)
    except Exception as err:
        logger.error(err)
    finally:
        mail.disconnect()


if __name__ == '__main__':
    send_new_password()
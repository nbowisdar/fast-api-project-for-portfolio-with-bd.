from pydantic import AnyHttpUrl
from .send_email import MyEmail
from loguru import logger
from src.utils.security.jwt.jwt_token import create_access_token
from src.utils.tools.config import MAIL_SENDER, MAIL_PASSWORD
from datetime import timedelta


def send_link(*, recv_mail, login, end_point: str,
              base_url: AnyHttpUrl = 'http://127.0.0.1:8000'):
    mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)
    data = {"sub": login,
            'position': 'user'}
    token = create_access_token(data, expires_delta=timedelta(minutes=3))
    msg = base_url + end_point + token
    try:
        mail.send_reset_link(recv_mail, msg, 'Reset password')
    except Exception as err:
        logger.error(err)
    finally:
        mail.disconnect()


def send_register_link(*, recv_mail, end_point: str, token: str,
                base_url: AnyHttpUrl = 'http://127.0.0.1:8000'):
    mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)
    msg = base_url + end_point + token
    try:
        mail.send_reset_link(recv_mail, msg, 'Your register link')
    except Exception as err:
        logger.error(err)
    finally:
        mail.disconnect()


# if __name__ == '__main__':
#     mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)
#     mail.send_reset_link('380992566619v@gmail.com', 'test_message')
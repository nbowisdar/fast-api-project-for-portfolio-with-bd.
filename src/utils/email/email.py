from .send_email import MyEmail
from loguru import logger
from src.utils.tools.config import MAIL_SENDER, MAIL_PASSWORD, BASE_URL


async def send_reset_link(*, recv_mail: str, end_point: str, token: str):
    mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)

    # create message
    msg = BASE_URL + end_point + token
    try:
        await mail.send_message(recv_mail, msg, 'Reset password')
    except Exception as err:
        logger.error(err)
    finally:
        mail.disconnect()


async def send_register_link(*, recv_mail, end_point: str, token: str):
    mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)

    # create message
    msg = BASE_URL + end_point + token
    try:
        await mail.send_message(recv_mail, msg, 'Your register link')
    except Exception as err:
        logger.error(err)
    finally:
        mail.disconnect()

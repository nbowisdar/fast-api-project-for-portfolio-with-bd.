from send_email import MyEmail
from loguru import logger
from src.utils.tools.config import MAIL_SENDER, MAIL_PASSWORD

def main():
    mail = MyEmail(MAIL_SENDER, MAIL_PASSWORD)
    try:
        mail_recv = '380992566619v@gmail.com'
        code = mail.generate_code()
        mail.send_code(code, mail_recv)

        #wait_and_reset('mark', code, p.update_password)
    except Exception as err:
        logger.error(err)
    finally:
        mail.disconnect()


if __name__ == '__main__':
    main()
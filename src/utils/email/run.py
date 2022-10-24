
from send_email import MyEmail
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def main():
    load_dotenv()
    mail = MyEmail(os.getenv('MAIL_SENDER'), os.getenv('MAIL_PASSWORD'))
    try:
        mail_recv = '380992566619v@gmail.com'
        code = mail.generate_code()
        mail.send_code(code, mail_recv)

        #wait_and_reset('mark', code, p.update_password)
    except Exception as err:
        logging.error(err)
    finally:
        mail.disconnect()


if __name__ == '__main__':
    main()
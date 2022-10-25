from os import getenv
from dotenv import load_dotenv
load_dotenv()

#project
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1000

#email_cred
MAIL_SENDER = getenv('MAIL_SENDER')
MAIL_PASSWORD = getenv('MAILPASSWORD')

# db_cred
DATABASE = getenv('DB_NAME')
HOST = getenv('DB_HOST')
USER = getenv('DB_USER')
PASSWORD = getenv('DB_PASSWORD')

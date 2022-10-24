from dotenv import load_dotenv
import os
from peewee import PostgresqlDatabase

load_dotenv()
db = PostgresqlDatabase(database=os.getenv('DB_NAME'),
                        host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'))

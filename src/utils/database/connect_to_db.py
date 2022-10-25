from peewee import PostgresqlDatabase
from src.utils.tools.config import DATABASE, HOST, USER, PASSWORD

db = PostgresqlDatabase(
    database=DATABASE,
    host=HOST,
    user=USER,
    password=PASSWORD
)

from fastapi import FastAPI, Path
from baseModels import UserModel
from work_with_db import connect
import json
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
psql = connect()


@app.get("/show_all")
async def hello():
    psql = connect()
    data = psql.show_data()
    psql.disconnect()
    return {json.dumps(data)}


@app.post('/create_user')
async def create_user(user: UserModel):
    try:
        psql.create_user(user.name, user.password, user.balance)
        logging.info(f'User created - {user.name}')
        return {f'User created - {user.name}'}

    except Exception as err:
        logging.error(err)
        logging.error('Wrong attempt to create user')
        return {'Wrong data user already exists'}

@app.put('/update_password')
def update_password(login: str, new_password: str):
    try:
        psql.update_password(login, new_password)
        logging.info(f'{login} - password update')
        return {f'{login} - password update'}

    except Exception as err:
        logging.error(err)
        logging.error('Wrong attempt to update password')
        return {'error'}





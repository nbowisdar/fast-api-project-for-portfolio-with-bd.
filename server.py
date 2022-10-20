from fastapi import FastAPI, Path
import baseModels as m
import new_db as db
import json
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/show_all")
async def show_all():
    data = db.show_all()
    return {data.json()}


@app.post('/create_user')
async def create_user(user: m.CreateUser):
    try:
        db.create_user(user.name, user.password, user.balance)
        logging.info(f'{user.name} - created')
        return {'ok'}

    except Exception as err:
        logging.error(err)
        logging.error('Wrong attempt to create user')
        return {'error'}

@app.delete('/drop_user')
async def drop_user(login: str):
    try:
        db.drop_user(login)
        return {'ok'}
    except Exception as err:
        logging.error(err)
        return {err}

@app.put('/update_balane')
def update_balance(login: str, tokens: int):
    try:
        db.update_balance(login, tokens)
        logging.info(f'{login} - balance update')
        return {'ok'}

    except Exception as err:
        logging.error(err)
        return {'error'}


@app.put('/update_password')
def update_password(login: str, new_password: str):
    try:
        db.update_password(login, new_password)
        logging.info(f'{login} - password update')
        return {'ok'}

    except Exception as err:
        logging.error(err)
        return {'error'}


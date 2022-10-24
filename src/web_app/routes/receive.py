from fastapi import status, HTTPException
from schemas.base_models import BaseUser
from src.utils.database import queries as db
import logging
from server import app


@app.get("/show_all")
async def show_all():
    data = db.show_all_users()
    return {data.json()}

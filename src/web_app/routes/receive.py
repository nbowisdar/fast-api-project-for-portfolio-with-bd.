from src.web_app.crud import queries as db
from server import app


@app.get("/show_all")
async def show_all():
    data = db.show_all_users()
    return {data.json()}

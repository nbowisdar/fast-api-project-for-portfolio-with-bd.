from fastapi import FastAPI

from src.web_app.routes.base_routes import base_router
from src.web_app.routes.root_points import root_router
from src.web_app.routes.users_point import users_router


app = FastAPI()

app.include_router(users_router)
app.include_router(root_router)
app.include_router(base_router)


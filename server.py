from fastapi import FastAPI
from src.web_app.routes.users_point import users_router
from src.web_app.routes.match_points import matches_router
from src.utils.security.jwt_token import jwt_router


app = FastAPI()

app.include_router(users_router)
app.include_router(matches_router)
app.include_router(jwt_router)


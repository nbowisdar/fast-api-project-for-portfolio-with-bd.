from pydantic import BaseModel, AnyHttpUrl


class SendLink(BaseModel):
    recv_mail = str
    login: str
    base_url: AnyHttpUrl = 'http://127.0.0.1:8000'
    end_point: str

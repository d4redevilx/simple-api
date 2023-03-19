from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    username: str
    full_name: str
    email: str
    disabled: bool = False

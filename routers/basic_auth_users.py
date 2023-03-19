from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict
from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool = False


class UserDB(User):
    hashed_password: str


app = FastAPI()

# autenticación
oauth2_scheme = OAuth2PasswordBearer('/login')

users_db = {
    "joe": {
        "username": "joe",
        "full_name": "Joe Doe",
        "email": "joedoe@mail.com",
        "disabled": False,
        "hashed_password": "fakehashed123456"
    },
    "mark": {
        "username": "mark",
        "full_name": "Mark Miller",
        "email": "markmiller@mail.com",
        "disabled": False,
        "hashed_password": "fakehashedqwerty"
    },
    "olivia": {
        "username": "olivia",
        "full_name": "Olivia Davids",
        "email": "oliviadavids@mail.com",
        "disabled": False,
        "hashed_password": "fakehashedsecret1"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def get_user(username: str) -> Dict:
    if username in users_db:
        return UserDB(**users_db[username])


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form_data.username, None)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')

    user = get_user(form_data.username)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail='Incorrect password'
        )

    return {"access_token": user.username, "token_type": "bearer"}


@app.get('/users/me')
async def read_user_me(user: User = Depends(get_current_active_user)):
    del user.hashed_password
    return user

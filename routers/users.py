from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}}
)


class User(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    age: int


fake_users = [User(id=1, name='Joe', lastname='Doe', email='joedoe@mail.com', age=35),
              User(id=2, name='Mark', lastname='Smith',
                   email='marksmith@mail.com', age=55),
              User(id=3, name='Oliver', lastname='Miller', email='olivermiller@mail.com', age=25)]


@router.get('/')
async def users(skip: int = 0, limit: int = 10):
    return fake_users[skip: skip + limit]


@router.get('/{id}')
async def get_user_by_id(id: int):
    user = search_user(id)
    if user:
        return user
    else:
        return {"error": f"No se ha encontrado un usuario con el id {id}"}


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if search_user(user.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User exist')

    fake_users.append(user)
    return user


@router.put('/')
async def update_user(user: User):

    for index, user_db in enumerate(fake_users):
        if user_db.id == user.id:
            fake_users[index] = user
            return {"message": "Usuario actualizado con éxito!", "user": user}

    return {"error": f"No se ha encontrado un usuario con el id {user.id}"}


@router.delete('/{id}')
async def delete_user(id: int):
    for index, user_db in enumerate(fake_users):
        if user_db.id == id:
            del fake_users[index]
            return {"message": "Usuario elminado con éxito!", "user": user_db}

    return {"error": f"No se ha encontrado un usuario con el id {id}"}


def search_user(id: int):
    user = list(filter(lambda user: user.id == id, fake_users))
    if len(user):
        return user[0]
    return None

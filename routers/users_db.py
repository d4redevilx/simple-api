from fastapi import APIRouter, HTTPException, status
from typing import List
from db.models.user import User
from db.schemas.user import user_schema
from bson.objectid import ObjectId
from db.client import db_client

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}}
)

fake_users = []


@router.get('/', response_model=List[User])
async def users(skip: int = 0, limit: int = 10):
    return list(map(user_schema, db_client.local.users.find().skip(skip).limit(limit)))


@router.get('/{id}')
async def get_user_by_id(id: str):
    user = db_client.local.users.find_one({"_id":  ObjectId(id)})
    if user:
        return User(**user_schema(user))
    else:
        return {"error": f"No user found with id {id}"}


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if search_user_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User exist')

    user_dict = user.dict()
    del user_dict['id']

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = User(**user_schema(db_client.local.users.find_one({"_id": id})))

    return new_user


@router.put('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def update_user(user: User):
    user_dict = user.dict()
    del user_dict['id']

    try:
        db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)},
            user_dict
        )

        new_user = User(
            **user_schema(db_client.local.users.find_one({"_id": ObjectId(user.id)}))
        )
        return new_user

    except:
        return {"error": f"No user found with id {id}"}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": f"No user found with id {id}"}


def search_user_by_email(email: str) -> User | None:
    try:
        user = db_client.local.users.find_one({"email": email})
        if user:
            return User(**user_schema(user))
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="An error occurred")

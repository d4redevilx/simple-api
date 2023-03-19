from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix='/products',
    tags=['Products'],
    responses={404: {'description': 'Not found'}}
)


class Product(BaseModel):
    id: int
    name: str


products_list = [
    Product(id=1, name='Producto 1'),
    Product(id=2, name='Producto 2'),
    Product(id=3, name='Producto 3'),
    Product(id=4, name='Producto 4'),
    Product(id=5, name='Producto 5')
]


@router.get('/')
async def get_all_products() -> List[Product]:
    return products_list


@router.get('/{id}', response_model=Product)
async def get_product_by_id(id: int) -> Product:
    return products_list[id]

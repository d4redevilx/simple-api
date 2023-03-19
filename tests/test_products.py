from fastapi.testclient import TestClient
from routers import products

client = TestClient(products.router)


def test_get_product_by_id():
    response = client.get('/products/0')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'name': 'Producto 1'
    }

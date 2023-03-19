from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users_db, jwt_auth_users

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users_db.router)
app.include_router(jwt_auth_users.router)

# Static
app.mount('/static', StaticFiles(directory='static'), name='static')

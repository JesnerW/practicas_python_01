# antes que nada, tener instalado fastapi para importarlo.
# pip install "fastapi[all]".
from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users
# para cargar y usar elementos estaticos, imagenes 
from fastapi.staticfiles import StaticFiles 

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
  return "!Hola FastAPI!"

# PARA LEVANTAR EL SERVIDOR
# uvicorn main:app --reload.
# main = archivo.
# app = instancia creada en la linea 5 de este documento.
# --reload = para que recargue en cada guardado.


# DOCUMENTACION GENERADA AUTOMATICAMENTE.
# http://127.0.0.1:8000/docs - generado automaticamente con Swagger.
# http://127.0.0.1:8000/redoc - generado automaticamente con Redocly.
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Entidad User

class User(BaseModel):
  id: int
  name: str
  surname: str
  url: str
  age: int

user_list = [
  User(id=1, name="Jesner", surname="Wilian", url="1.com", age=28),
  User(id=2, name="Jesner2", surname="Wilian2", url="2.com", age=22),
  User(id=3, name="Jesner3", surname="Wilian3", url="3.com", age=44)
]


# se crea una funcion
def buscar_user(id: int):
  users = filter(lambda user: user.id == id, user_list)
  try:
    return list(users)[0]
  except:
    return {"error": "El usuario no existe"}


@router.get("/users", status_code=200)
async def users():
  return user_list


# Ejemplo con PATH
# http://127.0.0.1:8000/userquery/2
@router.get("/user/{id}", response_model=User, status_code=200)
async def user(id: int):
  if type(buscar_user(id)) == User:
    return buscar_user(id)
  else:
    raise HTTPException(status_code=404, detail="El usuario no existe")


# Ejemplo con QUERY
# http://127.0.0.1:8000/userquery/?id=2
@router.get("/userquery/", response_model=User, status_code=200)
async def user(id: int):
  if type(buscar_user(id)) == User:
    return buscar_user(id)
  else:
    raise HTTPException(status_code=404, detail="El usuario no existe")


# Ejemeplo para guardar un Usuario usando la Clase User
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
  if type(buscar_user(user.id)) == User:
    raise HTTPException(status_code=204, detail="El ususario ya existe")
  else: 
    user_list.append(user)
    return user

# Ejemeplo actualizar un user usando clase User
@router.put("/user/", response_model=User, status_code=201)
async def user(user: User):

  found = False

  for index, saved_user in enumerate(user_list):
    if saved_user.id == user.id:
      user_list[index] = user
      found = True

  if not found:
    raise HTTPException(status_code=404, detail="El usuario no existe")
  else: 
    return user


# Eliminando Usuario con PATH
@router.delete("/user/{id}", status_code=200)
async def user(id: int):

  found = False

  for index, saved_user in enumerate(user_list):
    if saved_user.id == id:
      del user_list[index]
      found = True
      
  if not found:
    raise HTTPException(status_code=404, detail="El usuario no existe")
  else: 
    return {"detail": "Usuario con ID "+str(id)+" eliminado correctamente."}
      
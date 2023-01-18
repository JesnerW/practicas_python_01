# no olvidar instalar pip install "python-jose[cryptography]"
# no olvidar instalar pip install "passlib[bcrypt]"
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "3a7531d351ff6c030260a30da7e60edf36af5b3f2b5529f18d3d16fbe1c12516"

router = APIRouter(prefix="/jwt", 
                  tags=["Login JWT"],
                  responses={404: {"message":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
  username: str
  full_name: str
  email: str
  disabled: bool

class UserDB(User):
  password: str

users_db = {
  "jotace": {
    "username": "jotace",
    "full_name": "JesnerW",
    "email": "123@123.com",
    "disabled": False,
    "password": "$2a$12$rDbadjF3jIY9ONYWu//1nOnof6Y3w9mugh9lkS7zHd3o/vr3FV.5S"
  },
  "jotace2": {
    "username": "jotace2",
    "full_name": "JesnerW2",
    "email": "1233@1233.com",
    "disabled": True,
    "password": "$2a$12$YRQgxlP/IO9s/4aYbmiys.78NS6awfdU6WTi.4ikZ7aUISWinvocu"
  }
}

def search_user_db(username: str):
  if username in users_db:
    return UserDB(**users_db[username])

def search_user(username: str):
  if username in users_db:
    return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

  exception = HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED, 
      detail = "Credenciales de autenticacion invalidas", 
      headers = {"WWW-Authenticate": "Bearer"})

  try:
    username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
    if username is None:
      raise exception
  except JWTError:
    raise exception

  return search_user(username)

async def current_user(user: User = Depends(auth_user)):
  if user.disabled:
    raise HTTPException(
      status_code = status.HTTP_400_BAD_REQUEST, 
      detail = "Usuario inactivo")

  return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
  user_db = users_db.get(form.username)
  if not user_db:
    raise HTTPException(
      status_code = status.HTTP_400_BAD_REQUEST, 
      detail = "El usuario no es correcto")
  
  user = search_user_db(form.username)
  if not crypt.verify(form.password, user.password):
    raise HTTPException(
      status_code = status.HTTP_400_BAD_REQUEST, 
      detail = "La contraseña no es correcta")


  access_token = {
    "sub": user.username, 
    "exp" : datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION)}

  return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM, ) , "token_type" : "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
  return user
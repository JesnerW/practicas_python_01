from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/products", 
                  tags=["Products"],
                  responses={404: {"message":"No encontrado"}})

products_list = ["producto1", "producto2", "producto3", "producto4", "producto5", "producto6",]

@router.get("/", status_code=200)
async def users():
  return products_list


@router.get("/{id}", status_code=200)
async def users(id: int):
  return products_list[id]


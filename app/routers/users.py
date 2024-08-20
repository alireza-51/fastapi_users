from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, dependencies

router = APIRouter()

@router.post("/users/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(dependencies.get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@router.get("/users/", response_model=list[schemas.UserOut])
async def read_users(skip: int = 0, limit: int = 10, sort: str = "username", db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.get_users(db, skip=skip, limit=limit, sort=sort)

@router.get("/users/{user_id}", response_model=schemas.UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user: schemas.UserCreate, db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.update_user(db=db, user_id=user_id, user=user)

@router.delete("/users/{user_id}", response_model=schemas.UserOut)
async def delete_user(user_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    await crud.delete_user(db=db, user_id=user_id)
    return {"status": "success"}

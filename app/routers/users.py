from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app import crud, schemas, dependencies, database, auth
from app.models import User

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        return await crud.create_user(db=db, user=user)
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            if "email" in str(e.orig):
                raise HTTPException(status_code=400, detail="Email already registered")
            elif "username" in str(e.orig):
                raise HTTPException(status_code=400, detail="Username already registered")


@router.get("/users/", response_model=List[schemas.UserResponse])
async def read_users(offset: int = 0, limit: int = 10, sort: str = "username", db: AsyncSession = Depends(database.get_db)):
    return await crud.get_users(db, offset=offset, limit=limit, sort=sort)

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user: schemas.UserCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: User = Depends(auth.get_current_user)
):
    # Check if the current user is an admin or if they are updating their own information
    if current_user.role == "Admin" or current_user.id == user_id:
        return await crud.update_user(db=db, user_id=user_id, user=user)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this user.",
        )

@router.delete("/users/{user_id}", response_model=schemas.UserResponse, dependencies=[Depends(dependencies.admin_role_required)])
def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    return crud.delete_user(db=db, user_id=user_id)
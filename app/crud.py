from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app import models, schemas
from app.auth import get_password_hash

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, offset: int = 0, limit: int = 10, sort: str = "username"):
    result = db.execute(select(models.User).order_by(sort).offset(offset).limit(limit))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    stmt = update(models.User).where(models.User.id == user_id).values(
        username=user.username, email=user.email, password=get_password_hash(user.password)
    ).execution_options(synchronize_session="fetch")
    db.execute(stmt)
    db.commit()
    return await get_user(db, user_id)

async def delete_user(db: AsyncSession, user_id: int):
    user = delete(models.User).where(models.User.id == user_id).execution_options(synchronize_session="fetch")
    db.execute(user)
    db.commit()
    return True

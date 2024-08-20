from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from . import models, schemas
from .auth import get_password_hash

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10, sort: str = "username"):
    result = await db.execute(select(models.User).order_by(sort).offset(skip).limit(limit))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    stmt = update(models.User).where(models.User.id == user_id).values(
        username=user.username, email=user.email, password=get_password_hash(user.password)
    ).execution_options(synchronize_session="fetch")
    await db.execute(stmt)
    await db.commit()
    return await get_user(db, user_id)

async def delete_user(db: AsyncSession, user_id: int):
    stmt = delete(models.User).where(models.User.id == user_id).execution_options(synchronize_session="fetch")
    await db.execute(stmt)
    await db.commit()
    return True

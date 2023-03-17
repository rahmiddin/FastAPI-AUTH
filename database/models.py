from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer, MetaData, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import engine, async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession

metadata = MetaData()


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    child = relationship("Shop", uselist=False, backref="user")


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    state = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


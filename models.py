from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True)
    title = Column(String(255), nullable=False)
    completed = Column(Integer, default=0)

DATABASE_URI = 'postgresql+asyncpg://postgres:1234@localhost:5432/todo_app'
engine = create_async_engine(DATABASE_URI, echo=False)
SessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
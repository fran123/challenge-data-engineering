
import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, Relationship
from sqlalchemy import URL

class Departament(SQLModel,table=True):
    id: int = Field(primary_key=True)
    department: str = Field(nullable=False)

class Job(SQLModel,table=True):
    id: int = Field(primary_key=True)
    job: str = Field(nullable=False)

class Employee(SQLModel,table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    hire_datetime: datetime.datetime = Field(nullable=False)
    departament: Departament = Relationship()
    job: Job = Relationship()

url_object = URL.create(
    "postgresql",
    username="postgres",
    password="admin",  # plain (unescaped) text
    host="localhost",
    database="challenge",
)

engine = create_engine(url_object)

def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
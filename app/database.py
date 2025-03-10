
import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, Relationship
from sqlalchemy import URL
from app.config import settings

class Department(SQLModel,table=True):
    id: int = Field(primary_key=True)
    department: str = Field(nullable=False)

class Job(SQLModel,table=True):
    id: int = Field(primary_key=True)
    job: str = Field(nullable=False)

class Employee(SQLModel,table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=True)
    hire_datetime: datetime.datetime = Field(nullable=True)
    department_id: int = Field(nullable=True,foreign_key="department.id")
    job_id: int = Field(nullable=True,foreign_key="job.id")

url_object = URL.create(
    settings.db_driver,
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database,
)

engine = create_engine(url_object)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import URL
from app.database import get_session
from app.main import app
from app.database import Department,Job,Employee
from datetime import datetime

FILE_DEPARTMENTS_HISTORICAL = "./tests/files/departments.csv"
FILE_JOBS_HISTORICAL = "./tests/files/Jobs.csv" 
FILE_EMPLOYEES_HISTORICAL = "./tests/files/hired_employees.csv" 


@pytest.fixture(name="session")
def session_fixture():
    url_object = URL.create(
        "postgresql",
        username="postgres",
        password="admin",
        host="localhost",
        port="5432",
        database="challenge_test",
    )

    engine = create_engine(url_object)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_departments_historical(client: TestClient):
    response = client.post(
        "/departments/historical/", files = {'file': open(FILE_DEPARTMENTS_HISTORICAL, 'rb')}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["filename"] == "departments.csv"

def test_jobs_historical(client: TestClient):
    response = client.post(
        "/jobs/historical/", files = {'file': open(FILE_JOBS_HISTORICAL, 'rb')}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["filename"] == "Jobs.csv"

def test_employees_historical(session: Session,client: TestClient):
    load_departments(session)
    load_jobs(session)
    response = client.post(
        "/employees/historical/", files = {'file': open(FILE_EMPLOYEES_HISTORICAL, 'rb')}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["filename"] == "hired_employees.csv"

def test_metrics_number_employees_hired_by_department_by_job_by_quarter(
        session: Session,
        client: TestClient
):
    load_departments(session)
    load_jobs(session)
    load_employees(session)
    response = client.get(
        "/metrics/number_employees_hired_by_department_by_job_by_quarter?year=2021"
    )
    data = response.json()
    assert response.status_code == 200
    
    assert data[0]["department"] == "Product Management"
    assert data[0]["job"] == "Marketing Assistant"
    assert data[0]["q1"] == 0
    assert data[0]["q2"] == 0
    assert data[0]["q3"] == 0
    assert data[0]["q4"] == 2

    assert data[1]["department"] == "Product Management"
    assert data[1]["job"] == "VP Sales"
    assert data[1]["q1"] == 0
    assert data[1]["q2"] == 0
    assert data[1]["q3"] == 0
    assert data[1]["q4"] == 0

    assert data[2]["department"] == "Sales"
    assert data[2]["job"] == "Marketing Assistant"
    assert data[2]["q1"] == 0
    assert data[2]["q2"] == 0
    assert data[2]["q3"] == 0
    assert data[2]["q4"] == 0

    assert data[3]["department"] == "Sales"
    assert data[3]["job"] == "VP Sales"
    assert data[3]["q1"] == 0
    assert data[3]["q2"] == 1
    assert data[3]["q3"] == 0
    assert data[3]["q4"] == 0

def test_metrics_departments_with_employees_hired_more_than_mean(
        session: Session,
        client: TestClient
):
    load_departments(session)
    load_jobs(session)
    load_employees(session)
    response = client.get(
        "/metrics/departments_with_employees_hired_more_than_mean?year=2021"
    )
    data = response.json()
    assert response.status_code == 200
    
    assert data[0]["id"] == 1
    assert data[0]["department"] == "Product Management"
    assert data[0]["hired"] == 2


def load_departments(session:Session):
    session.add(Department(id=1, department="Product Management"))
    session.add(Department(id=2, department="Sales"))
    session.commit()

def load_jobs(session:Session):
    session.add(Job(id=1, job="Marketing Assistant"))
    session.add(Job(id=2, job="VP Sales"))
    session.commit()

def load_employees(session:Session):
    session.add(Employee(
        id=1, 
        name="Harold Vogt",
        hire_datetime=datetime(2021,11,7,9,30),
        department_id=1,
        job_id=1
    ))
    session.add(Employee(
        id=2, 
        name="Santiago Mendoza",
        hire_datetime=datetime(2021,11,7,10,30),
        department_id=1,
        job_id=1
    ))
    session.add(Employee(
        id=3, 
        name="Ty Hofer",
        hire_datetime=datetime(2021,5,3,9,30),
        department_id=2,
        job_id=2
    ))
    session.commit()

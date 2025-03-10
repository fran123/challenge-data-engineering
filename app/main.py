import uvicorn
from fastapi import FastAPI
from .routers import departments, jobs, employees,metrics
from .database import create_tables
from contextlib import asynccontextmanager

from sqlalchemy import text  ,create_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(employees.router)
app.include_router(metrics.router)


@app.get("/")
async def root():
    return {"response":"CHALLENGE DATA ENGINEERING"}

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


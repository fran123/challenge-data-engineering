import uvicorn
from fastapi import FastAPI
from .routers import departments, jobs, employees,metrics
from .database import create_tables
from contextlib import asynccontextmanager

from sqlalchemy import text  ,create_engine
app = FastAPI()

app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(employees.router)
app.include_router(metrics.router)

@asynccontextmanager
def lifespan():
    create_tables()

@app.get("/")
async def root():
    return {"response":"CHALLENGE DATA ENGINEERING"}

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


import uvicorn
from fastapi import FastAPI
from .routers import departments, jobs, employees
from .database import create_tables

from sqlalchemy import text  ,create_engine
app = FastAPI()

app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(employees.router)


@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
async def root():
    return {"response":"CHALLENGE DATA ENGINEERING"}

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


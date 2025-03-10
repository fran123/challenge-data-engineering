from fastapi import Depends,APIRouter,Query
from app.database import get_session
from sqlmodel import Field, Session, text
router = APIRouter(
    prefix="/metrics"
)

@router.get("/number_employees_hired_by_department_by_job_by_quarter")
async def number_employees_hired_by_department_by_job_by_quarter(
    year: int = Query(default=2021),
    session: Session = Depends(get_session)
): 
    query ="""
       WITH	
        metric AS (
            SELECT department_id,
                    job_id,
                    COUNT(id) filter (WHERE extract(MONTH FROM hire_datetime) between 1 and 3)  AS q1,
                    COUNT(id) filter (WHERE extract(MONTH FROM hire_datetime) between 4 and 6)  AS q2,
                    COUNT(id) filter (WHERE extract(MONTH FROM hire_datetime) between 7 and 9)   AS q3,
                    COUNT(id) filter (WHERE extract(MONTH FROM hire_datetime) between 10 and 12) AS q4
            FROM employee 
            WHERE EXTRACT(YEAR FROM hire_datetime) = :year
            GROUP BY department_id,
                    job_id
        )		
        SELECT 
            department.department 	AS department, 
            job.job 				AS job,
            COALESCE(metric.q1,0)  AS  q1,
            COALESCE(metric.q2,0)  AS  q2,
            COALESCE(metric.q3,0)  AS  q3,
            COALESCE(metric.q4,0)  AS  q4
        FROM department 
		CROSS JOIN job
        LEFT JOIN metric
        ON department.id = metric.department_id
		AND job.id = metric.job_id
        ORDER BY 
            department ASC,
            job ASC;

    """
    return session.connection().execute(text(query),dict(year=year)).mappings().all()


@router.get("/departments_with_employees_hired_more_than_mean")
async def number_employees_hired_by_department_by_job_by_quarter(
    year: int = Query(default=2021),
    session: Session = Depends(get_session)
):
    query = """
        WITH			  
            hired_by_department AS (
                SELECT department_id,
                    COUNT(*) hired
                FROM employee 
                WHERE EXTRACT(YEAR FROM hire_datetime) = :year
                AND department_id is not null
                GROUP BY department_id
            ),
            mean_hired_by_all_departments AS (
                SELECT 
                    department.id,
                    department.department,   
                    COALESCE(hired_by_department.hired,0) AS hired,  
                    AVG(COALESCE(hired_by_department.hired,0)) OVER () mean_hired
                FROM department
                LEFT JOIN hired_by_department
                ON department.id =hired_by_department.department_id 
            )
            SELECT 
                id,
                department,
                hired
            FROM mean_hired_by_all_departments
            WHERE hired > mean_hired
            ORDER BY hired DESC
    """
    return session.connection().execute(text(query),dict(year=year)).mappings().all()
  

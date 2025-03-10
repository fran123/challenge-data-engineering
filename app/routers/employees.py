from fastapi import Depends,APIRouter,UploadFile
from sqlmodel import Session
from app.database import get_session

router = APIRouter(
    prefix="/employees"
)

@router.post("/historical/")
async def historical(file: UploadFile,session: Session = Depends(get_session)):
    cursor = session.connection().connection.cursor()
    cursor.copy_from(file.file,table="employee",sep=",",null='')
    session.commit()
    return {"filename": file.filename} 




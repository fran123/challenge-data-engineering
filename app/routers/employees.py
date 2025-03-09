from fastapi import APIRouter,UploadFile

router = APIRouter(
    prefix="/employees"
)

@router.post("/historical/")
async def historical(file: UploadFile):
    return {"filename": file.filename}
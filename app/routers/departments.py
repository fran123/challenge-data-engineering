from fastapi import APIRouter,UploadFile

router = APIRouter(
    prefix="/departments"
)

@router.post("/historical/")
async def historical(file: UploadFile):
    return {"filename": file.filename}
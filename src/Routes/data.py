from fastapi import APIRouter,Depends,UploadFile
from helpers.config import get_settings,Settings
from controllers import DataController
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["Data","V1"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    
    is_valid=DataController().validate_upload_file(file=file)
    #is_valid=True
    return {
        "is_valid": is_valid
    }

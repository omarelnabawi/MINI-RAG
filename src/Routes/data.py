from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers import get_settings,Settings,response_signal
from controllers import DataController,ProjectController
import aiofiles
import os
import logging
logger = logging.getLogger("uvicorn.error")
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["Data","V1"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    data_controller=DataController()
    is_valid,response_signal=data_controller.validate_upload_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"response_signal": response_signal}
        )
    project_dir=ProjectController().get_project_dir(project_id=project_id)
    file_path,file_id=data_controller.generate_unique_filepath(original_filename=file.filename, project_id=project_id )
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunks :=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunks)
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"response_signal": response_signal}
        )
    return JSONResponse(
            content={"response_signal": response_signal,
                     "file_id": file_id
                    }
        )

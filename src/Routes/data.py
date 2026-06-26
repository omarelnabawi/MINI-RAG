from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers import get_settings,Settings
from models import response_signal
from controllers import DataController,ProjectController,Processcontroller
import aiofiles
import os
import logging
from Routes import process_request

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

#---------------------------------
@data_router.post("/process/{project_id}")
async def process_data(project_id:str,process_request:process_request):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    chunk_overlap=process_request.overlap_size
    process_controller=Processcontroller(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    file_chunks=process_controller.process_file_content(file_content=file_content,
                                                       file_id=file_id,
                                                       chunk_size=chunk_size,
                                                       chunk_overlap=chunk_overlap)
    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": response_signal.Chunking_Failed.value
            }
        )

    else:
        return file_chunks
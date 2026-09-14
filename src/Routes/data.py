from urllib import request

from fastapi import APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from helpers import get_settings,Settings
from models import response_signal
from controllers import DataController,ProjectController,Processcontroller
import aiofiles
import os
import logging
from Routes import process_request
from models import ProjectModel,ChunkModel,DataChunk
from models.db_schemes import Asset, project
from models.AssetModel import AssetModel
from models.enums import AssetTypeEnum
logger = logging.getLogger("uvicorn.error")
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["Data","V1"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project= await project_model.get_project_or_create_one(
        project_id=project_id
    )

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

    #store the assets into database
    asset_model=await AssetModel.create_instance(
        db_client=request.app.db_client
    )
    asset=Asset(
        asset_project_id=project.id,
        asset_name=str(file_id),
        asset_type=AssetTypeEnum.FILE.value,
        asset_size=os.path.getsize(file_path)
    )
    asset_record=await asset_model.create_asset(asset=asset)
    return JSONResponse(
            content={"response_signal": response_signal,
                     "file_id": file_id,
                     "asset_id": str(asset_record.id)
                    }
        )

#---------------------------------
@data_router.post("/process/{project_id}")
async def process_data(request:Request,project_id:str,process_request:process_request):
    #file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    chunk_overlap=process_request.overlap_size
    do_reset=process_request.do_reset

    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    chunk_model=await ChunkModel.create_instance(
        db_client=request.app.db_client
    )
    project= await project_model.get_project_or_create_one(
        project_id=project_id
    )
    process_controller=Processcontroller(project_id=project_id)
    asset_model=await AssetModel.create_instance(
        db_client=request.app.db_client
    )
    project_files_ids={}
    if process_request.file_id:
        asset_record=await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": response_signal.FILE_ID_ERROR.value
                }
            )
        
        project_files_ids={asset_record.id: asset_record.asset_name}
    else:
        asset_model=await AssetModel.create_instance(
            db_client=request.app.db_client
        )
        project_assets=await asset_model.get_all_project_assets(asset_project_id=project.id,asset_type=AssetTypeEnum.FILE.value)or [ ]
        project_files_ids={
            asset.id:asset.asset_name 
            for asset in project_assets}

    if len(project_files_ids)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": response_signal.No_Files_To_Process.value
            }
        )
    if do_reset==1:
           _=   await chunk_model.delete_chunks_by_project_id(project_id=project.id)
    num_chunks=0
    num_files=0
    for asset_id,file_id in project_files_ids.items():
        file_content=process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Failed to load content for file_id: {file_id}")
            continue  # Skip to the next file if content loading fails

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

        
        
        file_chunks_records=[
                DataChunk(
                        chunk_text=chunk.page_content,        
                        chunk_metadata=chunk.metadata,
                        chunk_order=i+1,
                        chunk_project_id=project.id,
                        chunk_asset_id=asset_id
                )
                for i, chunk in enumerate(file_chunks)
        ]
        
    
    
        num_chunks+=await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        num_files+=1
    return JSONResponse(
        content={
            "signal": response_signal.Chunking_Success.value,
            "num_chunks": num_chunks,
            "num_files": num_files,
            "num_chunks":num_chunks,
           #"File_chunks": [str(chunk.dict()) for chunk in file_chunks_records]
        }
    )
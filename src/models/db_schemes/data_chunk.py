from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunck_text:str=Field(...,min_length=1)
    chunck_metadata:dict
    chunck_order:int=Field(...,gt=0)
    chunck_project_id=ObjectId

    class Config:
        arbitrary_types_allowed=True
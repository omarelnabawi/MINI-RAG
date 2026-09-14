from pydantic import BaseModel, Field,validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str =Field(..., min_length=1, max_length=100)
    asset_name:str =Field(..., min_length=1, max_length=100)
    asset_size:Optional[int] =Field(None, gt=0)
    asset_config: Optional[dict] =Field(default=None)
    asset_pushed_at:Optional[datetime] =Field(default=datetime.utcnow)

    class Config:
            arbitrary_types_allowed=True
    
    @classmethod
    def get_indexs(cls):
            return [
                {
                    "key": [("asset_project_id  ", 1)],# 1 يعني تصاعدي
                    "name": "asset_project_id_index_1", # اسم المؤشر
                    "unique": False # project_id ممكن يتكرر في الassets المختلفة
                },
                {
                    "key": [("asset_project_id  ", 1),
                            ("asset_name", 1)],# 1 يعني تصاعدي
                    "name": "asset_project_id_name_index_1", # اسم المؤشر
                    "unique": True # project_id مش  هيتكرر في الassets المختلفة
                }   
            ]
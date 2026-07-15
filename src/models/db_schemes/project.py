from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id : str =Field(...,min_length=1)

    @validator('project_id')
    def validate_project_id(cls,value):
        if not value.isalnum:
            raise ValueError('Project_id must be alphanumaric')
        
        return value
    
    #الهدف من الجزء ده انه يخلي pydantic يتجاهل نوع ObjectId لانه مبيفهموش 
    class Config:
    
        arbitrary_types_allowed=True
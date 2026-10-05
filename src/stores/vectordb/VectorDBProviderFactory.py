from helpers import Settings
from .providers import QdrantDB
from .VectorDBEnums import  VectorDBType
from controllers.BaseController import BaseController

class VectorDBProviderFactory:
    def __init__(self,settings:Settings):
        self.settings=settings
        self.base_controller=BaseController()

    def create(self,provider:str):
        if provider==VectorDBType.QDRANT.value:
            db_path=self.base_controller.get_database_path(self.settings.VECTORDATABASE_QDRANT_DB_PATH)
            return QdrantDB(
                distancemethod=self.settings.VECTORDATABASE_DISTANCE_METHOD,
                db_path=db_path
            )
        return None
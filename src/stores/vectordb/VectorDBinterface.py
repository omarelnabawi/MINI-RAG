from abc import ABC,abstractclassmethod
from typing import List, Dict, Any
class VectorDBInterface(ABC):
    """
    Abstract base class for vector database interfaces.
    """
    @abstractclassmethod
    def connect(self):
        """
        Connect to the vector database.
        """
        pass

    @abstractclassmethod
    def disconnect(self):
        """
        Disconnect from the vector database.
        """
        pass

    @abstractclassmethod
    def is_collection_exists(self, collection_name) -> bool:
        """
        Check if a collection exists in the vector database.
        """
        pass

    @abstractclassmethod
    def list_all_collections(self) ->List:
        """
        List all collections in the vector database.
        """
        pass
    @abstractclassmethod
    def get_collection_info(self, collection_name:str) ->dict:
        """
        Get information about a specific collection from the vector database.
        """
        pass

    @abstractclassmethod
    def create_collection(self, collection_name: str, 
                          embedding_size: int, do_reset: bool = False):
        """
        Create a new collection in the vector database.
        """
        pass

    @abstractclassmethod
    def delete_collection(self, collection_name:str):
        """
        Delete a collection from the vector database.
        """
        pass

    @abstractclassmethod
    def insert_one(self,collection_name:str,
                   text:str,vector:list,metadata:dict=None,record_id:str=None):
        pass

    @abstractclassmethod
    def insert_many(self,collection_name:str,
                       texts:list,vectors:list,metadata:list=None,record_ids:list=None,
                       batch_size:int=50):
            pass

    @abstractclassmethod
    def search_by_vector(self,collection_name:str,
                         vector:list,limit:int):
        pass
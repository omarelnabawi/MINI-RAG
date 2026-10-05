from typing import List

from qdrant_client import QdrantClient,models
from ..VectorDBinterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnum
import logging

class QdrantDB(VectorDBInterface):
    def __init__(self,distancemethod:str,db_path:str):
        self.client=None
        self.db_path=db_path
        self.distancemethod=None

        if distancemethod==DistanceMethodEnum.COSINE.value:
            self.distancemethod=models.Distance.COSINE
        elif distancemethod==DistanceMethodEnum.DOT.value:
            self.distancemethod=models.Distance.DOT
        self.logger=logging.getLogger(__name__)

    def connect(self):
        self.client=QdrantClient(path=self.db_path)
        self.logger.info(f"Connected to QdrantDB at {self.db_path}")

    def disconnect(self):
        self.client=None
        self.logger.info("Disconnected from QdrantDB")

    def is_collection_exists(self,collection_name:str)->bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    
    def list_all_collections(self) ->List:
            return self.client.get_collections().collections
    def get_collection_info(self, collection_name:str) ->dict:
           return self.client.get_collection(collection_name=collection_name).dict()
    
        
    def create_collection(self, collection_name: str, 
                              embedding_size: int, do_reset: bool = False):
            if do_reset:
                    self.delete_collection(collection_name)
            if not self.is_collection_exists(collection_name):
                    _= self.client.create_collection(collection_name=collection_name,
                                                vectors=models.VectorParams(size=embedding_size,distance=self.distancemethod))
                    return True
            return False
                           
    
    def delete_collection(self, collection_name:str):
        if self.is_collection_exists(collection_name):
            self.client.delete_collection(collection_name=collection_name)
            self.logger.info(f"Collection {collection_name} deleted from QdrantDB")
        
    def insert_one(self,collection_name:str,
                       text:str,vector:list,metadata:dict=None,record_id:str=None):
            if not self.is_collection_exists(collection_name):
                  self.logger.error(f"Collection {collection_name} does not exist in QdrantDB")
                  return False
            try:
                _= self.client.upload_records(
                    collection_name=collection_name,
                    records=[
                        models.Record(
                            id=record_id,
                            vector=vector,
                            payload={"metadata": metadata, "text": text}
                        )
                    ]
                )
            except Exception as e:
                                    self.logger.error(f"Error occurred while uploading batch: {e}")
                                    return False
            return True
    def insert_many(self,collection_name:str,
                           texts:list,vectors:list,metadata:list=None,record_ids:list=None,
                           batch_size:int=50):
                if metadata is None:
                    metadata=[None]*len(texts)
                if record_ids is None:
                    record_ids=[None]*len(texts)
                for i in range(0, len(texts), batch_size):
                    batch_end=i + batch_size

                    batch_texts = texts[i:batch_end]
                    batch_vectors = vectors[i:batch_end]
                    batch_metadata = metadata[i:batch_end]
                    batch_records =[
                                 models.Record(
                                vector=batch_vectors[x],
                                payload={"metadata": batch_metadata[x], "text": batch_texts[x]})
                                for x in range(len(batch_texts))
                                                              ]
                    

                    try:
                        _= self.client.upload_records(
                                        collection_name=collection_name,
                                        records=batch_records)
                    except Exception as e:
                        self.logger.error(f"Error occurred while uploading batch: {e}")
                        return False
                return True
    def search_by_vector(self,collection_name:str,
                             vector:list,limit:int=5):
            return self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit
            )

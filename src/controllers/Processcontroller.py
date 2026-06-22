from controllers import BaseController,ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Routes import process_request  
class Processcontroller(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_dir(project_id=project_id)

    def get_file_extintion(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    def get_file_loader(self,file_id:str):
        file_extention=self.get_file_extintion(file_id=file_id)
        file_path=os.path.join(self.project_path,file_id)
        if file_extention == ProcessEnum.TXT.value:
            return TextLoader(file_path,encoding="utf-8")
        if file_extention == ProcessEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        return None
    def get_file_content(self,file_id:str):
        file_loader=self.get_file_loader(file_id=file_id)
        if file_loader is None:
            return None
        return file_loader.load()
    
    def process_file_content(self,file_content:list,file_id:str,chunk_size:int =100,
                             chunk_overlap:int=20):

        splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
            )
        file_content_text=[
            tx.page_content
            for tx in file_content
            ]
        file_content_metadata=[
            me.metadata
            for me in file_content
            ]
        chunks=splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
            )
        return chunks
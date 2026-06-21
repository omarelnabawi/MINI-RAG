
from .BaseController import BaseController
from helpers import response_signal
from fastapi import UploadFile
from .Projectcontroller import ProjectController
import os
import re
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.scale=1048576 # 1MB in bytes
    def validate_upload_file(self,file:UploadFile):   
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,response_signal.File_type_not_supported.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.scale:
            return False,response_signal.File_size_exceeded.value
        return True,response_signal.File_validate_sucess.value
    

    def generate_unique_filepath(self,original_filename:str,project_id:str):

        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_dir(project_id=project_id)

        cleaned_filename = self.clean_file_name(original_filename)
        new_filename = f"{random_filename}_{cleaned_filename}"
        new_file_path = os.path.join(project_path, new_filename)
        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_filename = f"{random_filename}_{cleaned_filename}"
            new_file_path = os.path.join(project_path, new_filename)
        return new_file_path,random_filename
   
   
    def clean_file_name(self,org_filename:str):
        # Remove any special characters and spaces from the filename
        cleaned_filename = re.sub(r'[^a-zA-Z0-9_.-]', '', org_filename)
        return cleaned_filename
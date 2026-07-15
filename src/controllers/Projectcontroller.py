from .BaseController import BaseController
import os
class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
    
    def get_project_dir(self,project_id):
        self.project_dir = os.path.join(self.Files_dir, project_id)
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
        return self.project_dir


from helpers.config import get_settings,Settings
import os
import string
import random
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.Files_dir = os.path.join(self.base_dir, 'assets', 'Files')

    def generate_random_string(self, length: int = 12):
        """Generate a random alphanumeric string."""
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return random_string
from ..config import Configuration
class ProcessData():
    config = None
    def __init__(self, config_file):
        self.config = Configuration(config_file)

    def process_data(self):
        self.create_users()
        self.create_sistema()

    def create_users(self):
        users = self.config.get_query_params("User")
        for user_params in users:
            from .service import UserService
            UserService(**user_params)

    def create_sistema(self):
        sistemas = self.config.get_query_params("Sistemas")
        for param in sistemas:
            from .service import SistemaService
            SistemaService(**param)
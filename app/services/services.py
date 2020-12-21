from app.config import Configuration
class ProcessData():
    config = None
    def __init__(self, config_file):
        self.config = Configuration(config_file)
        from app.models import Members, Games, db, User, Sistema
        self.db = db
        self.Members = Members
        self.Games = Games
        self.User = User
        self.Sistema = Sistema



    def process_data(self):
        self.create_users()
        self.create_sistema()

    def create_users(self):
        users = self.config.get_query_params("User")
        for user_params in users:
            user_exists = self.db.session.query(self.User).filter_by(username=user_params["username"]).count()
            if not user_exists:
                user = self.User(**user_params)
                self.db.session.add(user)
                self.db.session.commit()

    def create_sistema(self):
        sistemas = self.config.get_query_params("Sistemas")
        for param in sistemas:
            exists = self.db.session.query(self.Sistema).filter_by(nombre=param["nombre"]).count() == 1
            if not exists:
                sistema = self.Sistema(**param)
                self.db.session.add(sistema)
                self.db.session.commit()
from .factories.flask_instance import create_app

def create_full_app():
    app = create_app()
    return app
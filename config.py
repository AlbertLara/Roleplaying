class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {'development':DevelopmentConfig,
              'production':ProductionConfig}
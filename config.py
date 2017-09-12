import os

class Config():
    DEBUG = False

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DB = 'dshub'


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DB = 'dshub_test'


class ProductionConfig(Config):
    DEBUG = False



app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
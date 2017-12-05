# api/config.py

'''configuration settings for different app environments'''

import os

postgres_local_base = os.environ.get('DATABASE_URL_DEV') or \
                      'postgresql://postgres:arsenal2016@localhost/'
database_name = 'yummy_api'


class BaseConfig(object):
    '''Default configuration settings'''
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    '''Configurations for Testing, with a separate database'''
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'


class DevelopmentConfig(BaseConfig):
    '''Configurations for development'''
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    '''Configurations for production'''
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# dictionary for different app environments
app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}

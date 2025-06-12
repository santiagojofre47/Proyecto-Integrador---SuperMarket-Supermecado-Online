import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY',"123")
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'santi'
    MYSQL_DB = 'databd'
    DEBUG = True
    
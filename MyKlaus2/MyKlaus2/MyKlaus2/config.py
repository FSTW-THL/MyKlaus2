import configparser
import os
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../settings.ini"))

class Config:
    SECRET_KEY = config['DEFAULT']['SECRET_KEY']
    DOCUMENT_PATH = config['DEFAULT']['DOCUMENT_PATH']

    SQLALCHEMY_DATABASE_URI = config['Database']['URI']
    SQLALCHEMY_DATABASE_PORT = config['Database']['PORT']

    MAIL_SERVER = config['Mail']['SERVER']
    MAIL_PORT = config['Mail']['PORT']
    MAIL_USE_TLS = config['Mail']['SECRET_KEY']
    MAIL_USERNAME = config['Mail']['USER']
    MAIL_PASSWORD = config['Mail']['PASS']
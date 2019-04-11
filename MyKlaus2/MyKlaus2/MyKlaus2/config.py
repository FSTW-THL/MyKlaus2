import configparser
import os
from flask import url_for


config = configparser.ConfigParser()
#print({{url_for('static', filename='settings.ini')}})
#config.read(url_for('static', filename='settings.ini'))
config.read(os.getcwd()+"\MyKlaus2\static\settings.ini")

class Config:
    SECRET_KEY = config['DEFAULT']['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config['Database']['URI']
    MAIL_SERVER = config['Mail']['SERVER']
    MAIL_PORT = config['Mail']['Port']
    MAIL_USE_TLS = config['Mail']['SECRET_KEY']
    MAIL_USERNAME = config['Mail']['USER']
    MAIL_PASSWORD = config['Mail']['PASS']
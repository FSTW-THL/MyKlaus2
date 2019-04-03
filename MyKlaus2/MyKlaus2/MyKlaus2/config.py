import configparser


config = configparser.ConfigParser()
config.read('settings.ini')


class Config:
    SECRET_KEY = config['DEFAULT']['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config['Database']['URI']
    MAIL_SERVER = config['Mail']['SERVER']
    MAIL_PORT = config['Mail']['Port']
    MAIL_USE_TLS = config['Mail']['SECRET_KEY']
    MAIL_USERNAME = config['Mail']['USER']
    MAIL_PASSWORD = config['Mail']['PASS']
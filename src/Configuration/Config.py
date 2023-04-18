import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = ' rnasodjf fbj lasdfblkjbalkfdsjb bjbjljlakjsbdflkj p,cnvehkqu*/*-'


# class ProdConfig(Config):
#    DEBUG = False
#    TESTING = False
#    LOGIN_DISABLED = False
#
#
# class DevConfig(Config):
#    DEBUG = True
#    TESTING = True
#    LOGIN_DISABLED = False
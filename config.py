import os

SECRET_KEY = os.getenv("SECRET_KEY","defaultsecret")
#обовязкові зміни для SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///reddit.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

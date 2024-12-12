"""Flask configuration variables."""

from os import environ, path

# from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(BASE_DIR, ".env"))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    ENVIRONMENT = "development"
    APP_NAME = "flask_sqlalchemy_tutorial"

    # Flask Config
    FLASK_APP = "app.py"
    DEBUG = True
    SECRET_KEY = "YOURSECRET-KEY"

    # Database
    # mysql://root:12345678@127.0.0.1:3306/SecondTask
    SQLALCHEMY_DATABASE_URI = "mysql+pymmysql://root:12345678@127.0.0.1:3306/SecondTask"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


settings = Config

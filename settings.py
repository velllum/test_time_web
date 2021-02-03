import os
from environs import Env


env = Env()
env.read_env()

base_dir = os.path.abspath(os.path.dirname(__file__))
directory = os.path.join(base_dir, env.str("UPLOAD_FOLDER"))

class Configuration(object):
    DEBUG = env.bool("DEBUG", default=False)
    SECRET_KEY = env.str("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("MODIFICATIONS", default=True)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, env.str("DATABASE"))

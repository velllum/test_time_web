from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from settings import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


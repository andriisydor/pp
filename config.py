from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)

JWT_SECRET_KEY = 'super-secret'
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)
cors = CORS(app)

ADMIN_NAME = 'admin'

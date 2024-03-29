import os
from dotenv import dotenv_values
import pathlib

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# need import all the enitities before initializin db usin service_and_env import
import src.auth.entities as _
import src.file.entities as _
import src.wall.entities as _

from src.wall.client_controller import index
from src.wall.api_controller import index_api
from src.auth.controller import auth
from src.file.controller import file

import src.common.after_db_create as _
from src.common.session_and_env import env

env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath(".env").resolve())
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = env["JWT_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(env["JWT_ACCESS_TOKEN_EXPIRES"] or 900)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})  # acceptable for single server application

app.register_blueprint(index)
app.register_blueprint(index_api)
app.register_blueprint(auth)
app.register_blueprint(file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=bool(env["DEBUG"]))

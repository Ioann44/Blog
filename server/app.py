from dotenv import dotenv_values
import pathlib
from flask import Flask
from flask_jwt_extended import JWTManager
from src.wall.controller import index, index_api
from src.auth.controller import auth

env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath("docker/.env").resolve())
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = env["JWT_KEY"]
jwt = JWTManager(app)

app.register_blueprint(index)
app.register_blueprint(index_api)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(port=int(env["PORT"] or 5000), debug=bool(env["DEBUG"]))

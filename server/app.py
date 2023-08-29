from dotenv import dotenv_values
import pathlib
from flask import Flask
from wall.controller import index, index_api
from auth.controller import auth

env = dotenv_values(pathlib.Path(__file__).parent.parent.joinpath(".env").resolve())
app = Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(index_api)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(port=int(env["PORT"] or 5000), debug=bool(env["DEBUG"]))

import flask
from flask import Blueprint


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/create", methods=["POST"])
def create():
    json = flask.request.json
    return flask.Response(status=200)


@auth.route("/login", methods=["POST"])
def login():
    return flask.Response(status=200)

import flask
from flask import Blueprint
from flask import jsonify
from . import service


index = Blueprint("index", __name__)
index_api = Blueprint("index_api", __name__, url_prefix="/api")


@index.route("/")
def get_all():
    return flask.Response(status=200)


@index_api.route("/save", methods=["POST"])
def save():
    json = flask.request.json
    return flask.Response(status=200)


@index_api.route("/delete/<id>", methods=["POST"])
def delete(id):
    return flask.Response(status=200)

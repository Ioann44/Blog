from typing import Dict
import flask
from flask import Blueprint
from passlib.hash import bcrypt
from . import service

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/create", methods=["POST"])
def create():
    json: Dict[str, str] = flask.request.json or dict()
    success, user_id = service.create_user(
        service.entities.User(name=json["name"], hashed_password=bcrypt.hash(json["password"]))
    )
    if success:
        return {"id": user_id}
    else:
        return "Name already taken", 409


@auth.route("/login", methods=["POST"])
def login():
    json: Dict[str, str] = flask.request.json or dict()
    if "name" in json and "password" in json:
        success, user = service.get_user(json["name"])
        if success and user and bcrypt.verify(json["password"], user.hashed_password):  # type: ignore
            # return jwt with id
            return user.id.__str__()
        else:
            return "Name or password are incorrect", 401
    else:
        return "Name is not specified", 400

from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import jwt_required

from . import service

file = Blueprint("file", __name__, url_prefix="/file")


@file.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return "Haven't file field", 400
    file = request.files["file"]
    if not file.filename:
        return "Loading file not specified", 400

    saved = service.save_file(file)
    if saved is None:
        return "File not saved", 400
    else:
        return {"uuid": saved.name}


@file.route("/<string:name>")
def get_file(name: str):
    if not service.check_file_exists(name):
        return "File not exitst", 400
    else:
        directory = service.env["UPLOADS_RESOLVED_PATH"]
        assert directory is not None, "Unresolved uploads path"
        return send_from_directory(directory, name)


def set_connection_with_post():
    pass
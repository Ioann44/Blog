from typing import Any, Dict
import flask
from flask import Blueprint
from flask import jsonify
from . import service


index = Blueprint("index", __name__)
index_api = Blueprint("index_api", __name__, url_prefix="/api")


@index.route("/")
def get_all():
    return [
        {
            "id": p.id,
            "author_id": p.author_id,
            "theme": p.theme,
            "content": p.content,
            "likes": p.likes,
            "date": p.date,
        }
        for p in service.get_all()
    ]
    return flask.Response(status=200)


@index_api.route("/save", methods=["POST"])
def save():
    json: Dict[str, Any] = flask.request.json or dict()
    author_id = 1  # will be changed to jwt
    if not all([json.get("theme"), json.get("content")]):
        # extend to better description, if have time
        return flask.Response("Wrong data format, necessary field not specified or empty", status=400)

    post_dict = {
        "author_id": author_id,
        **{field: json[field] for field in ("theme", "content")},
    }

    # trying to update
    if "id" in json:
        try:
            id = int(json["id"])
        except ValueError:
            return flask.Response("Id must be a number", status=400)

        real_author_id = service.get_author_of_post(id)
        if real_author_id is None or real_author_id != author_id:
            # also prevents from creating with own id's and crashing later by autoincrement
            return flask.Response("Not authorized to change this post", status=401)
        else:
            post_dict["id"] = id

    saved_post = service.save(service.entities.Post(**post_dict))
    if saved_post is None:
        return flask.Response("Save failed", status=500)
    else:
        # return flask.Response(
        return {
            "id": saved_post.id,
            # only id yet, will be changed soon to username
            "author_id": saved_post.author_id,
            "theme": saved_post.theme,
            "content": saved_post.content,
            "likes": saved_post.likes,
            "date": saved_post.date,
        }
    # )


@index_api.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    author_id = 1  # also change to jwt

    real_author_id = service.get_author_of_post(id)
    if real_author_id is None or real_author_id != author_id:
        return flask.Response("Not authorized to delet this post", status=401)
    else:
        service.delete(id)
        return flask.Response("Post successfully deleted", status=200)

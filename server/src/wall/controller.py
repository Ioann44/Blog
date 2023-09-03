from typing import Any, Dict
import flask
from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from . import service


index = Blueprint("index", __name__)
index_api = Blueprint("index_api", __name__, url_prefix="/api")


@index.route("/")
def get_all():
    access_token = request.headers.get("Authorization")
    author_id = 0
    try:
        author_id = get_jwt_identity()
    except Exception:
        pass

    return [
        {
            "id": p.id,
            "author": p.author.name,
            "theme": p.theme,
            "content": p.content,
            "likes": p.likes,
            "date": p.date,
            "is_liked": is_liked,
            "files": [file.name for file in p.files],
        }
        for p, is_liked in service.get_all(author_id)
    ]


@index_api.route("/save", methods=["POST"])
@jwt_required()
def save():
    json: Dict[str, Any] = flask.request.json or dict()
    author_id = get_jwt_identity()
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
            return flask.Response("Not authorized to change this post", status=403)
        else:
            post_dict["id"] = id

    saved_post = service.save(service.entities.Post(**post_dict))
    if saved_post is None:
        return flask.Response("Save failed", status=500)

    # change files
    res_filenames = None
    if "filenames" in json:
        try:
            res_filenames = service.change_connected_post(json["filenames"], saved_post.id)  # type: ignore
        except:
            return flask.Response("Post is saved, but files not added: wrong filenames", status=400)

    return {
        "id": saved_post.id,
        "author": saved_post.author.name,
        "theme": saved_post.theme,
        "content": saved_post.content,
        "likes": saved_post.likes,
        "date": saved_post.date,
        "files": res_filenames or [],
    }


@index_api.route("/delete/<int:post_id>", methods=["POST"])
@jwt_required()
def delete(post_id):
    author_id = get_jwt_identity()

    real_author_id = service.get_author_of_post(post_id)
    if real_author_id is None or real_author_id != author_id:
        return flask.Response("Not authorized to delete this post", status=403)
    else:
        service.delete(post_id)
        return flask.Response("Post successfully deleted", status=200)


@index_api.route("/change_like/<int:post_id>", methods=["POST"])
@jwt_required()
def change_like(post_id):
    user_id = get_jwt_identity()
    is_liked_now, likes = service.change_likes(user_id, post_id)
    return {"is_liked": is_liked_now, "likes": likes}

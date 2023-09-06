from flask import Blueprint, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import pytz

from . import service
from ..auth import service as auth_service

index = Blueprint("index", __name__)


@index.route("/")
def get_redirection_page():
    return render_template("redirect.html")


@index.route("/index")
@jwt_required(optional=True)
def get_all():
    access_token = request.headers.get("Authorization")
    author_id = 0
    try:
        if access_token:
            author_id = get_jwt_identity()
    except Exception:
        pass

    authorized = bool(author_id)
    user_name = None

    if authorized:
        user_name = auth_service.get_name(author_id)
        if user_name is None:  # Authors can't be deleted, just in case
            authorized = False
        print(f"Author id: {author_id}, name: {user_name}")
    else:
        print(f"Not authorized")

    # set timezone
    desired_timezone = pytz.timezone("Etc/GMT-4")

    return render_template(
        "index_body.html",
        posts=[
            {
                "id": p.id,
                "author": p.author.name,
                "theme": p.theme,
                "content": p.content,
                "likes": p.likes,
                "date": p.date.astimezone(desired_timezone).strftime("%Y-%m-%d %H:%M"),
                "is_liked": is_liked,
                "files": [f"/file/{file.name}" for file in p.files],
            }
            for p, is_liked in service.get_all(author_id)
        ],
        authorized=authorized,
        user_name=user_name,
    )

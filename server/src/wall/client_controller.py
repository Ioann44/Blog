from flask import Blueprint, render_template, request
from flask_jwt_extended import get_jwt_identity

from . import service

index = Blueprint("index", __name__)


@index.route("/")
def get_all():
    access_token = request.headers.get("Authorization")
    author_id = 0
    try:
        author_id = get_jwt_identity()
    except Exception:
        pass

    return render_template(
        "index.html",
        posts=[
            {
                "id": p.id,
                "author": p.author.name,
                "theme": p.theme,
                "content": p.content,
                "likes": p.likes,
                "date": p.date,
                "is_liked": is_liked,
                "files": [f"/file/{file.name}" for file in p.files],
            }
            for p, is_liked in service.get_all(author_id)
        ],
    )

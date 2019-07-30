from flask import Blueprint, render_template, jsonify, request

import db
from utils import database
from utils.github import get_public_repos


bp = Blueprint("home", __name__)


@bp.route("/")
def home():
    """
    Render home page

    """
    return render_template("index.html")


@bp.route("/public_repos", methods=["GET"])
def public_repos():
    """
    List all public repos from github

    Returns (JSON): a list of repos and updated timestamp

    """
    repos, updated = get_public_repos()
    return jsonify({"repos": repos, "updated": updated})


@bp.route("/blogs", methods=["GET", "POST"])
def blogs():
    """
    GET or POST blogs

    Returns (JSON): GET  -> a list of all blogs
                    POST -> INFO message

    """
    db_conn = db.get_db()
    if request.method == "GET":
        all_blogs = database.get_blogs(db_conn)
        return jsonify({"blogs": all_blogs})
    title = request.json["title"]
    description = request.json["description"]
    url = request.json["url"]
    database.add_blog(db_conn, title, description, url)
    return jsonify({"INFO": "Blog added"})

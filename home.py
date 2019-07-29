from flask import Blueprint, render_template, jsonify

from utils.github import get_public_repos


bp = Blueprint("home", __name__)


@bp.route("/")
def hello():
    return render_template("index.html")


@bp.route("/public_repos")
def public_repos():
    repos, updated = get_public_repos()
    return jsonify({"repos": repos, "updated": updated})

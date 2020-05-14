from flask import Blueprint, request, jsonify
from flask_login import logout_user, login_user, current_user
from werkzeug.security import check_password_hash

from db import get_db
from utils.database import get_user

bp = Blueprint("auth", __name__)


@bp.route("/login_user", methods=["POST"])
def login():
    """
    GET -> Returns login page
    POST -> Try authenticating user

    """
    username = request.json["username"]
    password = request.json["password"]

    db_conn = get_db()
    user = get_user(db_conn, username)
    if not user or not check_password_hash(user.password, password):
        return jsonify({"logged_in": False})

    login_user(user, remember=True)
    return jsonify({"logged_in": True})


@bp.route("/logout")
def logout():
    """
    Logout current user

    """
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"logged_out": True})
    return jsonify({"logged_out": False})


@bp.route("/is_authenticated", methods=["GET"])
def is_authenticated():
    return jsonify({"is_authenticated": current_user.is_authenticated})

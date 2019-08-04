from werkzeug.security import check_password_hash
from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user

from db import get_db
from utils.database import get_user

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
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
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("home.home"))
    return redirect(url_for("auth.login"))


@bp.route("/admin", methods=["GET"])
@login_required
def admin():
    return render_template("admin.html")

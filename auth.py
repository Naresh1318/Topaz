from flask import Blueprint, request, render_template
from flask_login import login_required


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    render_template("login.html")


@bp.route("/admin", methods=["GET"])
@login_required
def admin():
    return "You seemed to be logged in!"

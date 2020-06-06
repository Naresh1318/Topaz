import datetime
import json
import subprocess

from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user

import db
from utils import database

bp = Blueprint("home", __name__)


@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"msg": "pong"})


@bp.route("/theme", methods=["GET"])
def theme():
    """
    Returns theme JSON object

    Returns (JSON): theme JSON object
    """
    try:
        with open(current_app.config["THEME_DIR"], "r") as f:
            data = json.load(f)
        return jsonify({"theme": data})
    except FileNotFoundError as e:
        return jsonify({"ERROR": e})


@bp.route("/top_k", methods=["GET"])
def top_k():
    """
    Returns the top k latest entries in the database

    Returns (JSON): a list of top k entries

    """
    db_conn = db.get_db()
    k = request.args.get("k")
    top_ks = database.get_top_k_entries(db_conn, int(k))
    db_conn.close()
    return jsonify({"top_k": top_ks})


@bp.route("/public_repos", methods=["GET", "POST"])
def public_repos():
    """
    List all public repos from github

    Returns (JSON): GET  -> a list of repos and updated timestamp
                    POST -> set visibility of projects

    """
    db_conn = db.get_db()
    if request.method == "GET":
        repos, updated = database.get_public_repos(db_conn)
        db_conn.close()
        return jsonify({"repos": repos, "updated": updated})
    if current_user.is_authenticated:
        selected = request.json["projects"]
        for s in selected:
            entry_id = s["id"]
            visible = s["visible"]
            database.update_visibility("public_repos", db_conn, entry_id, visible)
        db_conn.close()
        return jsonify({"INFO": "Updated"})
    return jsonify({"ERROR": "Unauthenticated"})


@bp.route("/blogs", methods=["GET", "POST"])
def blogs():
    """
    GET or POST blogs

    Returns (JSON): GET  -> a list of all blogs
                    POST -> INFO message

    """
    db_conn = db.get_db()
    if request.method == "GET":
        all_blogs, updated = database.get_articles(db_conn)
        db_conn.close()
        return jsonify({"blogs": all_blogs, "updated": updated})
    if current_user.is_authenticated:
        title = request.json["title"]
        description = request.json["description"]
        url = request.json["url"]
        image_url = request.json["image_url"]
        time_stamp = request.json["time_stamp"] + " 00:00:00"
        database.add_entry("blogs", db_conn, title, description, url, image_url, time_stamp)
        db_conn.close()
        return jsonify({"INFO": "Blog added"})
    return jsonify({"ERROR": "Unauthenticated"}), 401


@bp.route("/publications", methods=["GET", "POST"])
def publications():
    """
    GET or POST publications

    Returns (JSON): GET  -> a list of all publications
                    POST -> INFO message

    """
    db_conn = db.get_db()
    if request.method == "GET":
        all_blogs = database.get_entries("publications", db_conn)
        db_conn.close()
        return jsonify({"publications": all_blogs})
    if current_user.is_authenticated:
        title = request.json["title"]
        description = request.json["description"]
        url = request.json["url"]
        image_url = request.json["image_url"]
        time_stamp = request.json["time_stamp"] + " 00:00:00"
        database.add_entry("publications", db_conn, title, description, url, image_url, time_stamp)
        db_conn.close()
        return jsonify({"INFO": "Publication added"})
    return jsonify({"ERROR": "Unauthenticated"}), 401


@bp.route("/markdown_content", methods=["GET", "POST"])
def markdown_content():
    document_path = request.args.get("path")
    if ".." in document_path or "~" in document_path:
        return jsonify({"INFO": "Invalid path"}), 550
    local_path = f"{current_app.config['MARKDOWN_DIR']}/{document_path}"

    try:
        subprocess.run(["git", "checkout", "local"], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "checkout", "-b", "local"], check=True)

    if request.method == "GET":
        with open(local_path, "r") as f:
            subprocess.run(["git", "checkout", "-"])
            return jsonify({"INFO": "Document found", "markdown": f.read()})
    elif current_user.is_authenticated:
        content = request.json["markdown"]
        with open(local_path, "w") as f:
            f.write(content)

        # Commit changes
        try:
            saved_time = datetime.datetime.now()
            subprocess.run(["git", "add", local_path], check=True)
            subprocess.run(["git", "commit", "-m", f"{document_path}: {saved_time}"], check=True)
            subprocess.run(["git", "checkout", "-"])
            return jsonify({"INFO": "Document written", "time": str(saved_time)})
        except subprocess.CalledProcessError:
            subprocess.run(["git", "checkout", "-"])
            return jsonify({"INFO": "Document not written"})
    else:
        return jsonify({"ERROR": "Unauthenticated"}), 401

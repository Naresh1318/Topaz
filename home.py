import datetime
import json

from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user

import db
from utils import database
from utils.file_manager import FileManager, FileType

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
    if request.method == "GET":
        db_conn = db.get_db()
        repos, updated = database.get_public_repos(db_conn)
        db_conn.close()
        return jsonify({"repos": repos, "updated": updated})
    if current_user.is_authenticated:
        db_conn = db.get_db()
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
    GET all published blogs and external blog links

    Returns (JSON): GET  -> a list of all blogs
                    POST -> INFO message

    """
    if request.method == "GET":
        # external links
        db_conn = db.get_db()
        all_blogs, updated = database.get_articles(db_conn)
        db_conn.close()

        # internal blogs
        fm: FileManager = current_app.config["FILE_MANAGER"]
        published_files = fm.list(as_dict=True, file_type=FileType.PUBLISHED)
        published_files = list(published_files.values())
        all_blogs.extend(published_files)
        if current_user.is_authenticated:
            fm: FileManager = current_app.config["FILE_MANAGER"]
            unpublished_files = fm.list(as_dict=True, file_type=FileType.UNPUBLISHED)
            unpublished_files = list(unpublished_files.values())
            all_blogs.extend(unpublished_files)
        return jsonify({"blogs": all_blogs, "updated": updated})


@bp.route("/blogs/external_link", methods=["POST"])
def add_external_blog_link():
    if current_user.is_authenticated:
        db_conn = db.get_db()
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
    if request.method == "GET":
        db_conn = db.get_db()
        all_blogs = database.get_entries("publications", db_conn)
        db_conn.close()
        return jsonify({"publications": all_blogs})
    if current_user.is_authenticated:
        db_conn = db.get_db()
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
    file_name: str = request.args.get("path")
    file_type: FileType = FileType(int(request.args.get("file_type")))
    fm: FileManager = current_app.config["FILE_MANAGER"]
    if ".." in file_name or "~" in file_name or "/" in file_name:
        return jsonify({"INFO": "Invalid file name"}), 550

    if file_type == FileType.UNPUBLISHED and not current_user.is_authenticated:
        return jsonify({"ERROR": "Unauthenticated"}), 401

    if request.method == "GET":
        if request.args.get("version"):
            content = fm.read_version(file_name, request.args.get("version"), file_type)
        else:
            content = fm.read(file_name, file_type)
        return jsonify({"INFO": "Document found", "markdown": content})
    elif current_user.is_authenticated:
        content = request.json["markdown"]
        fm.write(file_name, content, file_type)
        return jsonify({"INFO": "Document written", "time": str(datetime.datetime.now())})
    else:
        return jsonify({"ERROR": "Unauthenticated"}), 401


@bp.route("/publish", methods=["GET"])
def publish():
    """
    Publish blog by moving file to published dir

    """
    if current_user.is_authenticated:
        file_name: str = request.args.get("path")
        fm: FileManager = current_app.config["FILE_MANAGER"]
        if ".." in file_name or "~" in file_name or "/" in file_name:
            return jsonify({"INFO": "Invalid file name"}), 550
        published = fm.publish(file_name=file_name)
        info = "published" if published else "not published"
        return jsonify({"INFO": info})
    return jsonify({"ERROR": "Unauthenticated"}), 401


@bp.route("/unpublish", methods=["GET"])
def unpublish():
    """
    Unpublish blog by removed it from published fir

    """
    if current_user.is_authenticated:
        file_name: str = request.args.get("path")
        fm: FileManager = current_app.config["FILE_MANAGER"]
        if ".." in file_name or "~" in file_name or "/" in file_name:
            return jsonify({"INFO": "Invalid file name"}), 550
        unpublished = fm.unpublish(file_name=file_name)
        info = "unpublished" if unpublished else "not unpublished"
        return jsonify({"INFO": info})
    return jsonify({"ERROR": "Unauthenticated"}), 401


@bp.route("/list_published", methods=["GET"])
def list_published():
    fm: FileManager = current_app.config["FILE_MANAGER"]
    published_files = fm.list(as_dict=True, file_type=FileType.PUBLISHED)
    return jsonify({"published": published_files})


@bp.route("/list_unpublished", methods=["GET"])
def list_unpublished():
    if current_user.is_authenticated:
        fm: FileManager = current_app.config["FILE_MANAGER"]
        unpublished_files = fm.list(as_dict=True, file_type=FileType.UNPUBLISHED)
        return jsonify({"unpublished": unpublished_files})
    return jsonify({"ERROR": "Unauthenticated"}), 401

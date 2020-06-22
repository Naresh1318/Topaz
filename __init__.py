import json
import os
import time

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from utils.database import get_user
from utils.file_manager import FileManager


# Change jinja template syntax
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


def create_app():
    """
    Initialize Flask and setup database

    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    app = CustomFlask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16),
        CACHED_TIME=time.time(),
        THEME_DIR="./data/theme.json",
        REAL_MARKDOWN_DIR=os.path.join(project_dir, "../topaz_docs"),
        MARKDOWN_DIR="./data/docs",
        FILE_MANAGER=FileManager(file_src_dir=os.path.join(project_dir, "../topaz_docs") + "/",
                                 symbolic_link_dst="./data/docs")
    )

    CORS(app, supports_credentials=True)

    # Init database
    import db
    db.init_db()

    # Init github cache
    from utils.github import update_public_repos
    db_conn = db.get_db()
    update_public_repos(db_conn)

    # Init meidum cache
    db_conn = db.get_db()
    with open(app.config["THEME_DIR"], "r") as f:
        data = json.load(f)
        medium_url = data["nav_bar_footer"]["medium"]["link"]
    from utils.medium import update_articles
    update_articles(db_conn, medium_url)

    # Register blueprints
    import home
    app.register_blueprint(home.bp)

    import auth
    app.register_blueprint(auth.bp)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(username):
        db_conn = db.get_db()
        return get_user(db_conn, username)

    return app

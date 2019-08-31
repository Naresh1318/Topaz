import os
import time
from flask import Flask
from flask_login import LoginManager

from utils.database import get_user


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
    app = CustomFlask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16),
        CACHED_TIME=time.time(),
        THEME_DIR="./data/theme.json"
    )

    # Init database
    import db
    db.init_db()

    # Init github cache
    from utils.github import update_public_repos
    db_conn = db.get_db()
    update_public_repos(db_conn)

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

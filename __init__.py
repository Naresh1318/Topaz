import os
import time
from flask import Flask


# Change jinja template syntax
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


def create_app():
    app = CustomFlask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",  # TODO: Change this
        CACHED_TIME=time.time()
    )

    # Init github cache
    from utils.github import cache_public_repos_request
    cache_public_repos_request()

    # Init database
    import db
    db.init_db()

    # Register blueprints
    import home
    app.register_blueprint(home.bp)

    return app

import os
import logging
import sqlite3
from werkzeug.security import generate_password_hash

database_path = "./data/topaz.sqlite"


def init_db():
    """
    Create database and tables if it isn't present

    """

    if os.path.exists(database_path):
        # Check if table blogs has the field 'automatically_added' or not
        # If not, add one
        try:
            db = get_db()
            c = db.cursor()
            # 1: True
            # NULL, 0: False
            c.execute('ALTER TABLE blogs ADD COLUMN automatically_added INTEGER')
        except Exception:
            logging.warning(
                "[W0002] Column 'automatically_added' is already exists. "
                "No need to add it."
            )
        db.commit()
        db.close()

        return
    # Create database and tables
    db = get_db()
    c = db.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    c.execute("CREATE TABLE public_repos (id INTEGER PRIMARY KEY, primary_language TEXT, primary_language_color TEXT, "
              "stars TEXT, title TEXT, description TEXT, readme TEXT, latest_commit TEXT, url TEXT, image_url TEXT, "
              "timestamp TEXT, visible INTEGER)")
    c.execute("CREATE TABLE blogs (id INTEGER PRIMARY KEY, title TEXT, description TEXT, "
              "url TEXT, image_url TEXT, timestamp TEXT, automatically_added INTEGER, "
              "file_type INTEGER, file_name TEXT)")
    c.execute("CREATE TABLE publications (id INTEGER PRIMARY KEY, title TEXT, description TEXT, "
              "url TEXT, image_url TEXT, timestamp TEXT, visible INTEGER)")

    # Create admin
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (os.getenv("USERNAME"),
                                                                       generate_password_hash(os.getenv("PASSWORD"))))
    db.commit()
    db.close()


def get_db():
    """
    Returns a database connection and sets output for be like dicts

    Returns (db object): sqlite3 db object

    """
    db = sqlite3.connect(database_path)
    db.row_factory = sqlite3.Row
    return db

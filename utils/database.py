import time
from flask import current_app

from utils.github import update_public_repos


# Cache data once every 15 minutes
cache_rate = 15 * 60  # sec


def get_public_repos(db_conn):
    """
    Returns a list of public repos from github
    Args:
        db_conn: sqlite3 db connection object

    Returns (repos, update_time): a list of repos and the last updated time

    """
    c = db_conn.cursor()
    start_time = current_app.config["CACHED_TIME"]
    if time.time() - start_time > cache_rate:
        current_app.config.from_mapping(CACHED_TIME=time.time())
        update_public_repos(db_conn)

    updated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    c.execute("SELECT * FROM public_repos")
    all_rows = c.fetchall()
    repos = [dict(row) for row in all_rows[::-1]]
    return repos, updated_time


def get_blogs(db_conn):
    """
    Returns a list of blogs from recent to old order
    Args:
        db_conn: sqlite3 db connection object

    Returns (list): a list of dicts with key as columns and values as table values

    """
    c = db_conn.cursor()
    c.execute("SELECT * FROM blogs")
    all_rows = c.fetchall()
    all_rows = [dict(row) for row in all_rows[::-1]]
    return all_rows


def add_blog(db_conn, title, description, url):
    """
    Adds entries as another row
    Args:
        db_conn: sqlite3 db connection object
        title (str): blog title
        description (str): blog description
        url (str): blog link

    Returns:

    """
    c = db_conn.cursor()
    try:
        c.execute("INSERT INTO blogs (title, description, url, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                  (title, description, url))
        db_conn.commit()
        db_conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    return True

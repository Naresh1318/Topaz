import datetime
import json
import logging
import time

from flask import current_app
from flask_login import UserMixin

from utils.github import update_public_repos
from utils.medium import update_articles

# Cache data once every 15 minutes
cache_rate = 15 * 60  # sec


class User(UserMixin):
    pass


def get_user(db_conn, username):
    """
    Returns UserMixin object if the username matches an entry in the data
    Args:
        db_conn: sqlite3 db connection object
        username (str): username string

    Returns (User): UserMixin Object with id set to username

    """
    c = db_conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user_row = c.fetchall()
    if not user_row:
        return None
    user = User()
    query_user = dict(user_row[0])
    user.id = query_user["username"]
    user.password = query_user["password"]
    return user


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

    updated_time = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    c.execute("SELECT * FROM public_repos")
    all_rows = c.fetchall()
    repos = [dict(row) for row in all_rows[::-1]]
    return repos, updated_time


def get_articles(db_conn):
    """
    Returns a list of article from medium
    Args:
        db_conn: sqlite3 db connection object
    """
    c = db_conn.cursor()
    start_time = current_app.config["CACHED_TIME"]
    if time.time() - start_time > cache_rate:
        current_app.config.from_mapping(CACHED_TIME=time.time())
        with open(current_app.config["THEME_DIR"], "r") as f:
            data = json.load(f)
        medium_url = data["medium_url"]
        update_articles(db_conn, medium_url)

    updated_time = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime(start_time)
    )
    c.execute("SELECT * FROM blogs")
    all_rows = c.fetchall()
    blogs = [dict(row) for row in all_rows[::-1]]
    return blogs, updated_time


def get_entries(table, db_conn):
    """
    Returns a list of entries from recent to old order
    Args:
        table (str): blogs, publications
        db_conn: sqlite3 db connection object

    Returns (list): a list of dicts with key as columns and values as table values

    """
    c = db_conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    all_rows = c.fetchall()
    all_rows = [dict(row) for row in all_rows[::-1]]
    return all_rows


def add_entry(table, db_conn, title, description, url, image_url, time_stamp):
    """
    Adds entry as another row
    Args:
        table (str): blogs, publications
        db_conn: sqlite3 db connection object
        title (str): blog title
        description (str): blog description
        url (str): blog link
        image_url (str): image link
        time_stamp (str): timestamp of the post

    Returns: True  -> entry added
             False -> error occurred

    """
    c = db_conn.cursor()
    try:
        if table == "blogs":
            c.execute(f"INSERT INTO {table} (title, description, url, image_url, timestamp, file_type) VALUES "
                      "(?, ?, ?, ?, ?, ?)",
                      (title, description, url, image_url, time_stamp, 1))
        else:
            c.execute(f"INSERT INTO {table} (title, description, url, image_url, timestamp) VALUES "
                      "(?, ?, ?, ?, ?)",
                      (title, description, url, image_url, time_stamp))
        db_conn.commit()
        db_conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    return True


def update_visibility(table, db_conn, entry_id, visibility):
    """
    Update visibility flag of entry
    Args:
        table (str): table name
        db_conn: sqlite3 db connection object
        entry_id (int): Row entry id to update
        visibility (int): visibility flag

    Returns (bool): True  -> Visibility updated
                    False -> Visibility not updated

    """
    c = db_conn.cursor()
    try:
        c.execute(f"UPDATE {table} SET visible = {int(visibility)} WHERE id={int(entry_id)}")
        db_conn.commit()
        db_conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    return True


def try_pop(l):
    """
    Try popping if not return a None dict
    Args:
        l: list to try pop'in

    Returns: popped value and list

    """
    try:
        value = l.pop(0)
    except IndexError:
        value = {"timestamp": None}
    return value, l


def max_times(times):
    """
    Returns the index of the max datetime
    Args:
        times (list): a list of datetimes in format 'YYYY-MM-DD HH:MM:SS'

    Returns: index of latest time

    """
    date_times = []
    for t in times:
        if t is None:
            date_times.append(datetime.datetime.now().replace(
                1970, 1, 1, 0, 0, 0))  # replace Nones with earliest date
            continue
        try:
            dt = []
            t = t.split("-")
            t = [i for i in t]
            for i in t:
                if ":" in i:
                    i = i.split(" ")
                    dt.append(i[0])
                    dt.extend([j.strip() for j in i[1].split(":")])
                else:
                    dt.append(i.strip())
            dt = list(map(int, dt))
            date_times.append(datetime.datetime.now().replace(*dt))
        except ValueError:
            logging.error(
                "[E0007] Error when parsing time. "
                "It is possible that the input time format is wrong.")
            date_times.append(
                datetime.datetime.now().replace(1970, 1, 1, 0, 0, 0))
    return date_times.index(max(date_times))


def get_top_k_entries(db_conn, k):
    """
    Returns a list of top k latest entries
    Args:
        db_conn: db connection object
        k (int): top k

    Returns: a list of top k entries

    """
    top_k = []
    repos, _ = get_public_repos(db_conn)
    blogs, _ = get_articles(db_conn)
    publications = get_entries("publications", db_conn)
    repo, repos = try_pop(repos)
    blog, blogs = try_pop(blogs)
    publication, publications = try_pop(publications)
    for _ in range(k):
        times = [repo["timestamp"], blog["timestamp"], publication["timestamp"]]
        latest_idx = max_times(times)
        if latest_idx == 0:
            top_k.append(repo)
            repo, repos = try_pop(repos)
        elif latest_idx == 1:
            top_k.append(blog)
            blog, blogs = try_pop(blogs)
        elif latest_idx == 2:
            top_k.append(publication)
            publication, publications = try_pop(publications)
    return top_k

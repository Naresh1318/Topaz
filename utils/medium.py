import json
import logging
from datetime import datetime

import requests


def update_articles(db_conn, medium_url):
    """
    Update database the list of articles which belongs to the user

    Args:
        db_conn: sqlite3 db connection
        medium_url: user's Meidum profile url

    Returns (dict): (no return)

    """
    c = db_conn.cursor()
    # Clear entries which are automatically added.
    # It means that manually added blogs are kept.
    c.execute("DELETE FROM blogs WHERE automatically_added = 1")
    try:
        retrieving_posts(medium_url, db_conn)
        db_conn.commit()
    except Exception as e:
        logging.error(f"[E0003] {e}")


def retrieving_posts(medium_url, db_conn):
    """
    Util for updating database the list of articles which belongs to the user

    Args:
        medium_url: user's Meidum profile url
        db_conn: sqlite3 db connection

    Returns (dict): (no return)

    """
    # Limit 10 used to bypass medium's cloudflare integration
    # https://github.com/gatsbyjs/gatsby/issues/17335
    api = medium_url + "/?format=json&limit=10"
    res = requests.get(api)
    if not res:
        raise Exception(
            '''[E0001] An error occured when crawling data by page''')

    content = json.loads(res.text.split("])}while(1);</x>")[1])
    posts = content['payload']['references']['Post']
    c = db_conn.cursor()
    for idx, post in enumerate(posts):
        post = posts[post]
        title = post["title"]
        description = post["content"]["subtitle"]
        url = medium_url + "/" + post["uniqueSlug"]

        previewImage = post["virtuals"]["previewImage"]
        if previewImage["imageId"]:
            image_url = "https://miro.medium.com/fit/c/%s/%s/%s" % (
                previewImage["originalWidth"],
                previewImage["originalHeight"],
                previewImage["imageId"])
        else:
            image_url = "/static/img/personal-website-logo.webp"

        try:
            time_stamp = datetime.fromtimestamp(int(post["createdAt"] / 1000))

        except Exception as e:
            time_stamp = ""
            logging.error(f"[E0006] {e}")

        try:
            c.execute(
                f"INSERT INTO blogs "
                "(title, description, url, image_url, timestamp, automatically_added, file_type) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, description, url, image_url, time_stamp, 1, 1))
            db_conn.commit()
        except Exception as e:
            logging.error(f"[E0004] {e}")

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

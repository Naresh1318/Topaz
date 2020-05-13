import json
import re

import requests

try:
    github_key = open("keys.txt", "r").readlines()[0].replace("\n", "")
    headers = {"Authorization": github_key}
except FileNotFoundError:
    print("ERROR: keys.txt not found. Ensure you have the keys place in the project root directory")


with open("data/github_language_colors.json") as f:
    github_language_colors = json.load(f)


def extract_first_image_url(readme):
    s = re.search(r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)", readme)
    if s is None:
        return ""
    return s.group()


def run_query(query):
    """
    A simple function to use requests.post to make the API call. Note the json= section.

    Args:
        query (str): GraphQL query to run

    Returns (JSON): response

    Reference: https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad

    """
    request = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run. Error code received {}: {}".format(request.status_code, query))


def update_public_repos(db_conn):
    """
    List all public repos along with their links and descriptions from the authenticated user and update db if needed

    Args:
        db_conn: sqlite3 db connection

    Returns (dict): See query below for the data format

    """
    query = """
    {
      viewer {
        repositories(privacy: PUBLIC, first: 100, orderBy: {field: PUSHED_AT, direction: ASC}) {
          totalCount
          nodes {
            name
            url
            description
            primaryLanguage {
              name
            }
            stargazers{
              totalCount
            }
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: 1) {
                    nodes {
                      committedDate
                      message
                    }
                  }
                }
              }
            }
            object(expression: "master:README.md") {
              ... on Blob {
                text
              }
            }
          }
        }
      }
    }
    """

    result = run_query(query)  # Execute the query
    c = db_conn.cursor()

    # Cache stored projects
    c.execute("SELECT * FROM public_repos")
    projects = c.fetchall()
    projects = {p["url"]: dict(p) for p in projects}

    c.execute("DELETE FROM public_repos")  # Clear all entries
    try:
        for node in result["data"]["viewer"]["repositories"]["nodes"]:
            title = node["name"]
            try:
                primary_language = node["primaryLanguage"]["name"]
                primary_language_color = github_language_colors[primary_language]["color"]
            except Exception as e:
                primary_language = "None"
                primary_language_color = "#FFFFFF"
            stars = node["stargazers"]["totalCount"]
            description = node["description"]
            readme = "" if node["object"] is None else node["object"]["text"]
            image_url = extract_first_image_url(readme)
            url = node["url"]
            latest_commit = node["defaultBranchRef"]["target"]["history"]["nodes"][0]["message"]
            timestamp = node["defaultBranchRef"]["target"]["history"]["nodes"][0]["committedDate"]\
                .replace("T", " ").replace("Z", "")  # Remove T and Z
            if url in projects:
                visible = projects[url]["visible"]
            else:
                visible = 1  # 1 -> True; 0 -> False
            c.execute("INSERT INTO public_repos "
                      "(title, primary_language, primary_language_color, stars, description, readme, "
                      "latest_commit, url, image_url, timestamp, visible) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (title, primary_language, primary_language_color, stars, description, readme, latest_commit, url,
                       image_url, timestamp, visible))
        db_conn.commit()
    except Exception as e:
        print(f"ERROR: {e}")

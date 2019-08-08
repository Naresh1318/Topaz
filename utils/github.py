import re
import requests


github_key = open("keys.txt", "r").readlines()[0].replace("\n", "")
headers = {"Authorization": github_key}


def extract_first_image_url(readme):
    s = re.search(r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)", readme)
    if s is None:
        return "/static/img/personal-website-logo.png"
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
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


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
    c.execute("DELETE FROM public_repos")  # Clear all entries
    try:
        for node in result["data"]["viewer"]["repositories"]["nodes"]:
            title = node["name"]
            description = node["description"]
            readme = "" if node["object"] is None else node["object"]["text"]
            image_url = extract_first_image_url(readme)
            url = node["url"]
            latest_commit = node["defaultBranchRef"]["target"]["history"]["nodes"][0]["message"]
            timestamp = node["defaultBranchRef"]["target"]["history"]["nodes"][0]["committedDate"]\
                .replace("T", " ").replace("Z", "")  # Remove T and Z
            c.execute("INSERT INTO public_repos (title, description, readme, latest_commit, url, image_url, timestamp) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (title, description, readme, latest_commit, url, image_url, timestamp))
        db_conn.commit()
        db_conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

import requests


github_key = open("keys.txt", "r").readlines()[0]
headers = {"Authorization": github_key}


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
            url = node["url"]
            latest_commit = node["defaultBranchRef"]["target"]["history"]["nodes"][0]["message"]
            timestamp = node["defaultBranchRef"]["target"]["history"]["nodes"][0]["committedDate"]\
                .replace("T", " ").replace("Z", "")  # Remove T and Z
            c.execute("INSERT INTO public_repos (title, description, latest_commit, url, timestamp) VALUES (?, ?, ?, ? ,?)",
                      (title, description, latest_commit, url, timestamp))
        db_conn.commit()
        db_conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

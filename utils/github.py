import os
import time
import pickle
import requests

from flask import current_app


cached_path = "./cached/repos_cached.pkl"
if not os.path.exists(cached_path):
    raise FileNotFoundError(f"{cached_path}: not found. "
                            f"Ensure that your github key is saved in the first line of this file")
github_key = open("keys.txt", "r").readlines()[0]
headers = {"Authorization": github_key}

# Cache data once every 15 minutes
cache_rate = 15 * 60  # sec


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


def cache_public_repos_request():
    """
    List all public repos along with their links and descriptions from the authenticated user

    Returns (dict): See query below for the data format

    """
    query = """
    {
      viewer {
        repositories(privacy: PUBLIC, first: 100, orderBy: {field: PUSHED_AT, direction: DESC}) {
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
    with open(cached_path, "wb") as f:
        pickle.dump(result["data"]["viewer"]["repositories"]["nodes"], f)


def get_public_repos():
    """
    Returns a list of public repos and the update time

    Returns: repos -> a list of repos with attributes
             updated_time -> time list was updated

    """
    start_time = current_app.config["CACHED_TIME"]
    if time.time() - start_time > cache_rate:
        current_app.config.from_mapping(CACHED_TIME=time.time())
        cache_public_repos_request()
    with open(cached_path, "rb") as f:
        repos = pickle.load(f)
    updated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    return repos, updated_time

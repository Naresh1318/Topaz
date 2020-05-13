import pytest

from __init__ import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    rv = client.get("/ping")
    assert rv._status_code == 200, "Failed to load home page"


def test_public_repos(client):
    rv = client.get("/public_repos")
    assert rv._status_code == 200, "Failed to load projects"


def test_blogs(client):
    rv = client.get("/blogs")
    assert rv._status_code == 200, "Failed to load blogs"


def test_publications(client):
    rv = client.get("/publications")
    assert rv._status_code == 200, "Failed to load publications"

import os.path
from http import HTTPStatus
import requests
from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5000"


def payload_model():
    return {
        "first_name": str(uuid4()),
        "last_name": str(uuid4()),
        "email": str(uuid4()) + "@mail.ru",
    }


def test_user_create():
    payload = payload_model()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    user_id = create_response.json()["id"]
    assert (
        create_response.json()["first_name"] == payload["first_name"]
        and create_response.json()["last_name"] == payload["last_name"]
        and create_response.json()["email"] == payload["email"]
    )
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert (
        get_response.json()["first_name"] == payload["first_name"]
        and get_response.json()["last_name"] == payload["last_name"]
        and get_response.json()["email"] == payload["email"]
    )
    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert (
        delete_response.status_code == HTTPStatus.OK
        and delete_response.json()["first_name"] == payload["first_name"]
        and delete_response.json()["last_name"] == payload["last_name"]
        and delete_response.json()["email"] == payload["email"]
        and delete_response.json()["status"] == "deleted"
    )


def test_user_create_wrong_data():
    payload = payload_model()
    payload["email"] = "some_wrong_emailmail.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_user_posts():
    test_users = []
    for _ in range(2):
        payload = payload_model()
        create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_user_response.status_code == HTTPStatus.CREATED
        test_users.append(create_user_response.json()["id"])
    test_posts = []
    post = {"author_id": test_users[0], "text": "Test"}
    for _ in range(2):
        create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post)
        test_posts.append(create_post_response.json()["id"])
    react = {"user_id": test_users[1], "reaction": "Test"}
    react_post_response = requests.post(
        f"{ENDPOINT}/posts/{test_posts[0]}/reaction", json=react
    )
    assert react_post_response.status_code == HTTPStatus.OK
    for mode in ["asc", "desc"]:
        get_response = requests.get(
            f"{ENDPOINT}/users/{test_users[0]}/posts", json={"sort": mode}
        )
        sorted_posts = get_response.json()["posts"]
        if mode == "asc":
            assert isinstance(sorted_posts, list) and all(
                sorted_posts[x]["reactions"] <= sorted_posts[x + 1]["reactions"]
                for x in range(len(sorted_posts) - 1)
            )
        else:
            assert isinstance(sorted_posts, list) and all(
                sorted_posts[x]["reactions"] >= sorted_posts[x + 1]["reactions"]
                for x in range(len(sorted_posts) - 1)
            )
    for i in range(2):
        delete_user_response = requests.delete(f"{ENDPOINT}/users/{test_users[i]}")
        assert delete_user_response.status_code == HTTPStatus.OK
        delete_post_response = requests.delete(f"{ENDPOINT}/posts/{test_posts[i]}")
        assert delete_post_response.status_code == HTTPStatus.OK


def test_leaderboard():
    n = 3
    test_users = []
    for _ in range(n):
        payload = payload_model()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.CREATED
        test_users.append(create_response.json()["id"])
    payload = {"type": "list", "sort": ""}
    for mode in ["asc", "desc"]:
        payload["sort"] = mode
        get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
        leaderboard = get_response.json()["users"]
        if mode == "asc":
            assert (
                isinstance(leaderboard, list)
                and all(
                    leaderboard[x]["total_reactions"]
                    <= leaderboard[x + 1]["total_reactions"]
                    for x in range(len(leaderboard) - 1)
                )
                and len(leaderboard) == n
            )
        else:
            assert (
                isinstance(leaderboard, list)
                and all(
                    leaderboard[x]["total_reactions"]
                    >= leaderboard[x + 1]["total_reactions"]
                    for x in range(len(leaderboard) - 1)
                )
                and len(leaderboard) == n
            )
    payload = {"type": "graph"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    leaderboard = get_response.text
    assert leaderboard == '<img src = "/static/leaderboard.png">' and os.path.exists(
        "app/static/leaderboard.png"
    )
    os.remove("app/static/leaderboard.png")
    for i in range(n):
        delete_response = requests.delete(f"{ENDPOINT}/users/{test_users[i]}")
        assert delete_response.status_code == HTTPStatus.OK

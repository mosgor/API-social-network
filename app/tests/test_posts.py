from http import HTTPStatus
import requests
from uuid import uuid4
from app.tests.test_users import payload_model

ENDPOINT = "http://127.0.0.1:5000"


def test_post_create():
    payload = payload_model()
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_user_response.status_code == HTTPStatus.CREATED
    user_id = create_user_response.json()["id"]
    post = {"author_id": user_id, "text": str(uuid4())}
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=post)
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json()["id"]
    assert (
        create_response.json()["author_id"] == post["author_id"]
        and create_response.json()["text"] == post["text"]
    )
    get_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert (
        get_response.json()["author_id"] == post["author_id"]
        and get_response.json()["text"] == post["text"]
    )
    delete_response = requests.delete(f"{ENDPOINT}/posts/{post_id}")
    assert (
        delete_response.status_code == HTTPStatus.OK
        and delete_response.json()["author_id"] == post["author_id"]
        and delete_response.json()["text"] == post["text"]
        and delete_response.json()["status"] == "deleted"
    )
    requests.delete(f"{ENDPOINT}/users/{user_id}")


def test_reactions():
    test_users = []
    for _ in range(2):
        payload = payload_model()
        create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_user_response.status_code == HTTPStatus.CREATED
        test_users.append(create_user_response.json()["id"])
    post_id = requests.post(
        f"{ENDPOINT}/posts/create", json={"author_id": test_users[0], "text": "Text"}
    ).json()["id"]
    reaction = {"user_id": test_users[0], "reaction": "text"}
    assert (
        requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=reaction).status_code
        == HTTPStatus.BAD_REQUEST
    )
    reaction["user_id"] = test_users[1]
    assert (
        requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=reaction).status_code
        == HTTPStatus.OK
    )
    for user_id in test_users:
        requests.delete(f"{ENDPOINT}/users/{user_id}")
    requests.delete(f"{ENDPOINT}/posts/{post_id}")

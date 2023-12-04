from app import app, USERS, POSTS, models
from flask import request, Response, url_for
from http import HTTPStatus
import matplotlib.pyplot as plt
import requests
from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5000"


def payload_model():
    return {
        "first_name": "Name" + str(uuid4()),
        "last_name": "Surname" + str(uuid4()),
        "email": "some_email" + str(uuid4()) + "@mail.ru",
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


def test_user_create_wrong_data():
    payload = payload_model()
    payload["email"] = "some_wrong_emailmail.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_user_posts():
    payload = payload_model()
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_user_response.status_code == HTTPStatus.CREATED
    first_user_id = create_user_response.json()["id"]
    post = {"author_id": first_user_id, "text": "Test"}
    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post)
    first_post_id = create_post_response.json()["id"]
    requests.post(f"{ENDPOINT}/posts/create", json=post)
    payload = payload_model()
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_user_response.status_code == HTTPStatus.CREATED
    second_user_id = create_user_response.json()["id"]
    react = {"user_id": second_user_id, "reaction": "Test"}
    react_post_response = requests.post(
        f"{ENDPOINT}/posts/{first_post_id}/reaction", json=react
    )
    assert react_post_response.status_code == HTTPStatus.OK
    get_response = requests.get(
        f"{ENDPOINT}/users/{first_user_id}/posts", json={"sort": "asc"}
    )
    sorted_posts = get_response.json()["posts"]
    assert (
        isinstance(sorted_posts, list)
        and all(
            sorted_posts[x]["reactions"] <= sorted_posts[x + 1]["reactions"]
            for x in range(len(sorted_posts) - 1)
        )
    )
    get_response = requests.get(
        f"{ENDPOINT}/users/{first_user_id}/posts", json={"sort": "desc"}
    )
    sorted_posts = get_response.json()["posts"]
    assert (
        isinstance(sorted_posts, list)
        and all(
            sorted_posts[x]["reactions"] >= sorted_posts[x + 1]["reactions"]
            for x in range(len(sorted_posts) - 1)
        )
    )

from app import app, USERS, models, POSTS
from flask import request, Response
import json
from http import HTTPStatus


@app.post("/posts/create")
def post_create():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]
    if not models.User.is_valid_id(author_id):
        return Response("There is no such user", status=HTTPStatus.NOT_FOUND)
    post = models.Post(post_id, author_id, text)
    POSTS.append(post)
    USERS[author_id].add_post(post_id)
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response("There is no such post", status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def react(post_id):
    data = request.get_json()
    user_id = data["user_id"]
    reaction = data["reaction"]
    if not models.User.is_valid_id(user_id) or not models.Post.is_valid_id(post_id):
        return Response("There is no such post or user", status=HTTPStatus.NOT_FOUND)
    if user_id == POSTS[post_id].author_id:
        return Response(
            "User can't react on his own post", status=HTTPStatus.BAD_REQUEST
        )
    POSTS[post_id].add_reaction(reaction)
    return Response(status=HTTPStatus.OK)

from app import app, USERS, POSTS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt


@app.post("/users/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    if not models.User.is_valid_email(email):
        return Response("Invalid or already used email", status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response("There is no such user", status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/posts")
def sort_posts(user_id):
    data = request.get_json()
    sort_type = data["sort"]
    unsorted_posts = {}
    for post_num in USERS[user_id].get_posts():
        if POSTS[post_num].status != "deleted":
            unsorted_posts[post_num] = POSTS[post_num].get_reactions_count()
    if sort_type == "asc":
        sorted_values = sorted(unsorted_posts.values())
    elif sort_type == "desc":
        sorted_values = sorted(unsorted_posts.values(), reverse=True)
    else:
        return Response("Wrong type of sorting", status=HTTPStatus.BAD_REQUEST)
    sorted_posts = {}
    for i in sorted_values:
        for j in unsorted_posts.keys():
            if unsorted_posts[j] == i:
                sorted_posts[j] = unsorted_posts[j]
    posts = [POSTS[x].to_dict() for x in sorted_posts.keys()]
    response = Response(
        json.dumps({"posts": posts}),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_leaderboard():
    data = request.get_json()
    leaderboard_type = data["type"]
    if leaderboard_type == "list":
        type_of_sort = data["sort"]
        if type_of_sort == "asc":
            leaderboard = [
                user.to_dict() for user in sorted(USERS) if user.status != "deleted"
            ]
        elif type_of_sort == "desc":
            leaderboard = [
                user.to_dict()
                for user in sorted(USERS, reverse=True)
                if user.status != "deleted"
            ]
        else:
            return Response("Wrong type of sorting", status=HTTPStatus.BAD_REQUEST)
        return Response(
            json.dumps({"users": leaderboard}),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
    elif leaderboard_type == "graph":
        fig, ax = plt.subplots()
        user_names = [user.get_name() for user in USERS if user.status != "deleted"]
        user_reactions = [
            user.get_total_reactions() for user in USERS if user.status != "deleted"
        ]
        ax.bar(user_names, user_reactions)
        ax.set_ylabel("User reactions")
        ax.set_title("User leaderboard by reactions")
        plt.savefig("app/static/leaderboard.png")
        return Response(
            f"""<img src = "{url_for('static', filename='leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    else:
        return Response("Wrong type of leaderboard", status=HTTPStatus.BAD_REQUEST)


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    user.status = "deleted"
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
                "status": user.status,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response

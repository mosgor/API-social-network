from app import app, USERS, POSTS


@app.get("/")
def init():
    response = (
        f"<h1>Hello World!</h1>"
        f"USERS:<br>{'<br>'.join([user.repr() for user in USERS])}<br>"
        f"POSTS:<br>{'<br>'.join([post.repr() for post in POSTS])}<br>"
    )
    return response

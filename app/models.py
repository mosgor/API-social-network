import re
from app import USERS, POSTS


class User:
    all_emails = set()

    def __init__(
        self, user_id, first_name, last_name, email, total_reactions=0, posts=None
    ):
        if posts is None:
            posts = []
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts

    @staticmethod
    def is_valid_email(email):
        if (
            isinstance(email, str)
            and re.match(r"[^@]+@[^@]+\.[^@]+", email)
            and email not in User.all_emails
        ):
            User.all_emails.add(email)
            return True
        return False

    @staticmethod
    def is_valid_id(user_id):
        return isinstance(user_id, int) and 0 <= user_id < len(USERS)

    def add_post(self, post):
        self.posts.append(post)

    def increase_reactions(self):
        self.total_reactions += 1

    def repr(self):
        return f"{self.id} {self.first_name} {self.last_name}"

    def get_posts(self):
        return self.posts

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
        }

    def get_name(self):
        return f"{self.first_name} {self.last_name} ({self.id})"

    def get_total_reactions(self):
        return self.total_reactions


class Post:
    def __init__(self, post_id, author_id, text, reactions=None):
        if reactions is None:
            reactions = []
        self.id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = reactions

    @staticmethod
    def is_valid_id(post_id):
        return isinstance(post_id, int) and 0 <= post_id < len(POSTS)

    def add_reaction(self, reaction):
        self.reactions.append(reaction)
        USERS[self.author_id].increase_reactions()

    def repr(self):
        return f"Own id: {self.id} author id: {self.author_id} {self.text}"

    def get_reactions_count(self):
        return len(self.reactions)

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        }

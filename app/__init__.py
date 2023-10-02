from flask import Flask

app = Flask(__name__)

USERS = []
POSTS = []

from app import views_all
from app import models
from app import views

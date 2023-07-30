from flask import Blueprint

bp = Blueprint("music", __name__)

from app.music import routes
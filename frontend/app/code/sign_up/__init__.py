from flask import Blueprint

bp = Blueprint('sign_up', __name__)

from . import routes
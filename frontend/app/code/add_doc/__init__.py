from flask import Blueprint

bp = Blueprint('add_doc', __name__)

from . import routes
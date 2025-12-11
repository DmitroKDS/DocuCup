from flask import Blueprint

bp = Blueprint('log_in', __name__)

from . import routes
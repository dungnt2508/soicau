from flask import Blueprint, g

bp = Blueprint('bp', __name__)

from . import auth
from . import main
from . import events

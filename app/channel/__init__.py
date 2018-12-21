from flask import Blueprint

channel = Blueprint('channel', __name__)

from . import controllers

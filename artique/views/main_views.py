from flask import Blueprint, url_for
from werkzeug.utils import redirect
from flask_smorest import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('user._list'))
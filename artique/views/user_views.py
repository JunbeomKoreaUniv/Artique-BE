from flask import Blueprint, jsonify
from flask_smorest import Blueprint
from artique.models import User

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/list')
def _list():
    user_list = User.query.order_by(User.email)
    users = [{"id": user.id, "email": user.email, "password": user.password, "nickname": user.nickname} for user in user_list]
    return jsonify(users)

@bp.route('/<int:user_id>')
def detail(user_id):
    user = User.query.get_or_404(user_id)
    user = {"id": user.id, "email": user.email, "password": user.password, "nickname": user.nickname}
    return jsonify(user)
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from artique import db

from artique.models import User

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/signup', methods=['POST'])
def signUp():
    data = request.get_json()
    email = User.query.filter_by(email=data['email']).first()
    nickname = User.query.filter_by(nickname=data['nickname']).first()

    if not email and not nickname:
        user = User(
            email=data['email'],
            nickname=data['nickname'],
            password=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": user.nickname + " Successfully signed up!"}), 201
    elif email and not nickname:
        return jsonify({"error": "Email already exists"}), 400
    elif not email and nickname:
        return jsonify({"error": "Nickname already exists"}), 400
    else:
        return jsonify({"error": "Email and nickname already exist"}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        # 사용자 email을 identity로 설정하여 토큰 생성
        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# 새로운 Access Token 발급 with Refresh Token
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_email = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_email)
    return jsonify(access_token=new_access_token), 200

@bp.route('/jwt-test', methods=['GET'])
@jwt_required()
def jwtTest():
    current_user_email = get_jwt_identity()
    return jsonify(logged_in_as=current_user_email), 200
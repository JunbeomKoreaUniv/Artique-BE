from flask import Blueprint, jsonify, request, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from artique import db

from artique.models import User, Picture
from artique.s3upload import upload_file_to_s3

bp = Blueprint('admin', __name__, url_prefix='/admin')

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

        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.headers["Access-Token"] = access_token
        response.headers["Refresh-Token"] = refresh_token
        return response
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# 새로운 Access Token 발급 with Refresh Token
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_email = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_email)

    response = make_response(jsonify({"message": "Token refreshed"}), 200)
    response.headers["Access-Token"] = new_access_token
    return response

@bp.route('/jwt-test', methods=['GET'])
@jwt_required()
def jwtTest():
    current_user_email = get_jwt_identity()
    return jsonify(logged_in_as=current_user_email), 200

@bp.route('/upload_picture', methods=['POST'])
def upload_picture():
    print(request.files)
    photo_file = request.files['picture_photo']
    sound_file = request.files['sound']

    print(photo_file, sound_file)

    # S3에 파일 업로드
    if photo_file:
        photo_file_url = upload_file_to_s3(photo_file, current_app.config["S3_BUCKET_NAME"], folder="pictures")
    if sound_file:
        sound_file_url = upload_file_to_s3(sound_file, current_app.config["S3_BUCKET_NAME"], folder="sounds")

    # 데이터베이스에 URL 저장
    new_picture = Picture(
        user_id=request.form.get("user_id"),  # user_id 전달 필요
        name=request.form.get("name"),
        artist=request.form.get("artist"),
        gallery=request.form.get("gallery"),
        start_date=request.form.get("start_date"),
        end_date=request.form.get("end_date"),
        custom_prompt=request.form.get("custom_prompt"),
        custom_explanation=request.form.get("custom_explanation"),
        custom_question=request.form.get("custom_question"),
        sound=sound_file_url,
        picture_photo=photo_file_url  # URL 저장
    )
    db.session.add(new_picture)
    db.session.commit()

    return jsonify({"message": "Picture uploaded successfully", "photo_url": photo_file_url, "sound_url": sound_file_url}), 200
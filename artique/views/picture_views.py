from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from .. import db
from ..models import Picture, User
from flask_jwt_extended import jwt_required, get_jwt_identity

from artique.s3upload import upload_file_to_s3

bp = Blueprint('picture', __name__, url_prefix='/picture')

@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    print("Create start")
    try:
        # 현재 로그인한 사용자의 이메일 가져오기
        user_email = get_jwt_identity()

        # User 테이블에서 해당 ID를 가진 사용자 조회
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # request에서 사진, 사운드 가져오고 S3에 파일 업로드
        photo_file = request.files['picture_photo']

        if photo_file:
            photo_file_url = upload_file_to_s3(photo_file, current_app.config["S3_BUCKET_NAME"], folder="pictures")

        # 날짜 변환
        start_date = datetime.strptime(request.form.get("start_date"), '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(request.form.get("end_date"), '%Y-%m-%d %H:%M')

        # Picture 인스턴스 생성
        picture = Picture(
            user_id=user.id,
            name=request.form.get("name"),
            artist=request.form.get("artist"),
            gallery=request.form.get("gallery"),
            start_date=start_date,
            end_date=end_date,
            custom_prompt=request.form.get("custom_prompt"),
            custom_explanation=request.form.get("custom_explanation"),
            custom_question=request.form.get("custom_question"),
            # sound=sound_file_url,
            picture_photo=photo_file_url
        )
        db.session.add(picture)
        db.session.commit()

        return jsonify({
            "message": "Picture created successfully",
            "picture_id": picture.id,
            "photo_url": photo_file_url
        }), 201

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"message": "Invalid date format. Use 'YYYY-MM-DD HH:MM'"}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



@bp.route('/modify/<int:picture_id>', methods=['POST'])
@jwt_required()
def modify(picture_id):
    picture = Picture.query.get_or_404(picture_id)

    # 현재 로그인한 사용자의 이메일 가져오기
    user_email = get_jwt_identity()

    # picture.user_id를 통해 email 정보 가져오기
    user_email_from_picture = User.query.filter_by(id=picture.user_id).first().email

    # 이메일 주소 비교
    if user_email_from_picture != user_email:
        return jsonify({"message": "Permission denied"}), 403

    # request에서 사진, 사운드 가져오고 S3에 파일 업로드
    photo_file = request.files['picture_photo']

    if photo_file:
        photo_file_url = upload_file_to_s3(photo_file, current_app.config["S3_BUCKET_NAME"], folder="pictures")

    # 날짜 변환
    start_date = datetime.strptime(request.form.get("start_date"), '%Y-%m-%d %H:%M')
    end_date = datetime.strptime(request.form.get("end_date"), '%Y-%m-%d %H:%M')

    try:
        picture.name = request.form.get("name")
        picture.artist = request.form.get("artist")
        picture.gallery = request.form.get("gallery")
        picture.start_date = start_date
        picture.end_date = end_date
        picture.custom_explanation = request.form.get("custom_explanation")
        picture.custom_question = request.form.get("custom_question")
        picture.picture_photo = photo_file_url

        db.session.commit()

        return jsonify({"message": "Picture updated successfully", "photo_url": photo_file_url}), 200

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"message": "Invalid date format. Use 'YYYY-MM-DD HH:MM'"}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
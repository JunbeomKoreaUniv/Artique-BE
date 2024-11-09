from datetime import datetime
from flask import Blueprint, request, jsonify
from .. import db
from ..models import Picture, User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

bp = Blueprint('picture', __name__, url_prefix='/picture')

@bp.route('/create/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()

    try:
        # 현재 로그인한 사용자의 ID 가져오기
        user_id = get_jwt_identity()

        # User 테이블에서 해당 ID를 가진 사용자 조회
        user = User.query.filter_by(email=user_id).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Picture 인스턴스 생성
        picture = Picture(
            name=data['name'],
            artist=data['artist'],
            gallery=data['gallery'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d %H:%M'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d %H:%M'),
            custom_explanation=data['custom_explanation'],
            custom_question=data['custom_question'],
            sound=data['sound'],
            user=user
        )
        db.session.add(picture)
        db.session.commit()

        return jsonify({
            "message": "Picture created successfully",
            "picture_id": picture.id
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

    # 현재 로그인한 사용자의 ID 가져오기
    user_id = get_jwt_identity()

    # picture.user_id를 통해 email 정보 가져오기
    user_email = User.query.filter_by(id=picture.user_id).first().email

    # 이메일 주소 비교
    if user_email != user_id:
        return jsonify({"message": "Permission denied"}), 403

    # 요청 데이터 가져오기
    data = request.get_json()
    try:
        picture.name = data['name']
        picture.artist = data['artist']
        picture.gallery = data['gallery']
        picture.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d %H:%M')
        picture.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d %H:%M')
        picture.custom_explanation = data['custom_explanation']
        picture.custom_question = data['custom_question']
        picture.sound = data['sound']

        db.session.commit()

        return jsonify({"message": "Picture updated successfully"}), 200

    except KeyError as e:
        return jsonify({"message": f"Missing key: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"message": "Invalid date format. Use 'YYYY-MM-DD HH:MM'"}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
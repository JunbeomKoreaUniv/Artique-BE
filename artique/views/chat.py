from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from artique import db

from artique.models import Chat

bp = Blueprint('chat', __name__, url_prefix='/chat')

# Chat 데이터 저장하는 API 엔드포인트
@bp.route('/save', methods=['POST'])
def save_chat():
    data = request.get_json()

    try:
        new_chat = Chat(
            picture_id=data['picture_id'],
            message=data['message'],
            sender=data['sender'],
            receiver=data['receiver']
        )
        db.session.add(new_chat)
        db.session.commit()

        return jsonify({'message': 'Chat saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
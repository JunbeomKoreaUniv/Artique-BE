import openai
from flask import Blueprint, jsonify, request
from artique import db
from artique.models import Chat
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

bp = Blueprint('chat', __name__, url_prefix='/chat')

# Chat 데이터 저장하는 API 엔드포인트
@bp.route('/save', methods=['POST'])
def save_chat():
    data = request.get_json()

    try:
        # 새로운 채팅 데이터 저장
        new_chat = Chat(
            picture_id=data['picture_id'],
            message=data['message'],
            sender=data['sender'], # sender: 사용자 nickname or "AI"
            receiver=data['receiver'] # receiver: 사용자 nickname or "AI"
        )
        db.session.add(new_chat)
        db.session.commit()

        if data['message']:
            # AI API 호출
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",  # 사용할 모델 이름 (예: gpt-3.5-turbo 등)
                messages=[{"role": "user", "content": data['message']}],
                max_tokens=150
            )

            # AI 응답을 DB에 저장
            gpt_response = response.choices[0].message.content.strip()
            print(gpt_response)

            gpt_chat = Chat(
                picture_id=data['picture_id'],  # 동일한 picture_id 사용
                message=gpt_response,  # AI 응답 메시지
                sender="AI",  # 발신자는 AI
                receiver=data['sender']  # 수신자는 원래 메시지의 sender
            )
            db.session.add(gpt_chat)
            db.session.commit()

        return jsonify({'message': gpt_response}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

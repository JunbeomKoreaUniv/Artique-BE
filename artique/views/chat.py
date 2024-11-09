import openai
from flask import Blueprint, jsonify, request
from artique import db
from artique.models import Chat, Sentence
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

        prompting = "너가 고흐라고 생각하고 말해줘. 말투도 좀 옛날사람처럼 말해줘. " + data['message']

        if prompting:
            # AI API 호출
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",  # 사용할 모델 이름 (예: gpt-3.5-turbo 등)
                messages=[{"role": "user", "content": prompting}],
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

# Chat 데이터 추출해서 요약한 뒤, 5개 Sentence를 저장 및 반환하는 API 엔드포인트
@bp.route('/summary', methods=['POST'])
def summarize_chat():
    data = request.get_json()
    receiver_id = data['receiver']

    try:
        # 채팅 데이터 추출
        chats = Sentence.query.join(Chat).filter(Chat.receiver == receiver_id).all()
        print(chats)
        chat_text = ' '.join([chat.chat.message for chat in chats])
        chat_text += '이 내용을 바탕으로 감성적인 문장들과 명언을 5개 만들어줘. 5개의 문장을 list로 반환해줘.'

        # AI API 호출
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",  # 사용할 모델 이름 (예: gpt-3.5-turbo 등)
                messages=[{"role": "user", "content": chat_text}],
                max_tokens=300
            )

        # AI 응답을 DB에 저장
        gpt_response = response.choices[0].message.content.strip()

        # AI 응답을 Sentence로 분리해서 DB에 저장
        sentences = gpt_response.split('\n')
        for sentence in sentences[2:-2]:
            new_sentence = Sentence(
                receiver_id=receiver_id,
                summary=sentence[3:]
            )
            db.session.add(new_sentence)
        db.session.commit()

        return jsonify({'sentences': sentences[2:-2]}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# 모든 Sentence 데이터를 반환하는 API 엔드포인트
@bp.route('/all_sentences', methods=['GET'])
def get_all_sentences():
    try:
        # 모든 Sentence 데이터 조회
        sentences = Sentence.query.all()

        sentence_list = []
        for sentence in sentences:
            sentence_list.append({
                "id": sentence.id,
                "summary": sentence.summary
            })

        return jsonify({"sentences": sentence_list}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
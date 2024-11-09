from flask import Blueprint, jsonify
from artique import db
from sqlalchemy import text
from artique.models import Sentence

bp = Blueprint('database', __name__, url_prefix='/database')

# 모든 테이블의 데이터 조회 API 엔드포인트
@bp.route('/all_data', methods=['GET'])
def get_all_data():
    try:
        # 모든 테이블 이름 조회
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
        tables = [row[0] for row in result]

        all_data = {}
        for table_name in tables:
            # 각 테이블의 데이터 조회
            table_data = db.session.execute(text(f"SELECT * FROM {table_name}")).mappings().all()
            # 데이터를 딕셔너리 형식으로 변환
            table_data_list = [dict(row) for row in table_data]
            all_data[table_name] = table_data_list

        return jsonify(all_data), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# sentence 테이블에 10개의 하드코딩된 데이터 추가 API 엔드포인트
@bp.route('/add_sentences', methods=['POST'])
def add_sentences():
    sentences = [
        {"chat_id": 1, "receiver_id": "배고픈 두더지", "summary": "밤하늘을 올려다볼 때, 별들은 고독 속에서 빛나는 희망을 속삭여준다. 내 그림 속 별들이 그랬던 것처럼."},
        {"chat_id": 2, "receiver_id": "배고픈 망아지", "summary": "고통 속에서 그려진 그림은, 누군가의 마음에 닿아 그를 위로할 힘을 가진다."},
        {"chat_id": 3, "receiver_id": "ㅁㄴㅇ", "summary": "내 삶이란 하늘에 남긴 붓질이었을 뿐, 그러나 그 별빛이 누군가의 마음에 닿는다면 그걸로 충분하지 않을까."},
        {"chat_id": 4, "receiver_id": "ㅁㄴㅇㅇ", "summary": "밤하늘은 내 감정이 머무는 캔버스였고, 별빛은 그 위에 남긴 내 위로였다."},
        {"chat_id": 5, "receiver_id": "김", "summary": "비록 아무도 나의 그림을 이해하지 못했지만, 시간이 흘러 그 안의 빛을 알아봐 주는 이가 있으니, 내 삶이 헛되지 않았다고 믿고 싶다."},
        {"chat_id": 6, "receiver_id": "이", "summary": "사이프러스 나무는 땅에서 하늘로 이어진 다리였다. 그곳으로 오르면 고통에서 벗어나 별의 노래를 들을 수 있을 것 같았다."},
        {"chat_id": 7, "receiver_id": "박", "summary": "예술은 세상과 연결되는 내 유일한 다리였고, 나는 밤하늘에 내 마음을 올려놓아 그 누구에게도 전해지길 바랐다."},
        {"chat_id": 8, "receiver_id": "최", "summary": "내가 남긴 붓질 하나하나가 세월을 넘어 사람들에게 닿아, 그들의 마음 속 별처럼 빛나길 바란다."},
        {"chat_id": 9, "receiver_id": "현", "summary": "내 작품을 보며 누군가가 위로받는다면, 나는 별이 속삭이는 하늘에서 그 마음을 함께 느낄 것이다."},
        {"chat_id": 1, "receiver_id": "우",
         "summary": "희망은 언제나 별빛 속에 존재하고, 하늘을 바라보는 자는 그 희망을 발견할 수 있다"}
    ]

    try:
        # sentence 테이블에 데이터 추가
        for sentence_data in sentences:
            new_sentence = Sentence(
                chat_id=sentence_data["chat_id"],
                receiver_id=sentence_data["receiver_id"],
                summary=sentence_data["summary"]
            )
            db.session.add(new_sentence)

        db.session.commit()

        return jsonify({"message": "10 sentences added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

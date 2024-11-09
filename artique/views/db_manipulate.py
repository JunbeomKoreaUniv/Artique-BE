from flask import Blueprint, jsonify
from artique import db
from sqlalchemy import text

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

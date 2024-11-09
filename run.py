import os
from artique import create_app, db

app = create_app()

# 데이터베이스 초기화 (필요시 실행)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render의 PORT 환경 변수를 사용
    app.run(host="0.0.0.0", port=port, debug=True)  # 모든 인터페이스에서 접근 가능하게 설정

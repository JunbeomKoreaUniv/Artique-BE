from flask import Blueprint, jsonify, request, current_app
from artique.s3upload import upload_file_to_s3

bp = Blueprint('combined_picture', __name__, url_prefix='/combined_picture')

@bp.route('/upload_combined_picture', methods=['POST'])
def upload_combined_picture():
    # 업로드된 파일 처리
    combined_file = request.files['combined_picture']  # 사진+글귀가 합쳐진 파일

    # S3에 파일 업로드
    try:
        combined_file_url = upload_file_to_s3(combined_file, current_app.config["S3_BUCKET_NAME"], folder="combined_pictures")
    except Exception as e:
        return jsonify({"error": f"Failed to upload to S3: {str(e)}"}), 500

    # URL만 프론트엔드에 반환
    return jsonify({ "message": "Combined picture uploaded successfully", "photo_url": combined_file_url }), 200
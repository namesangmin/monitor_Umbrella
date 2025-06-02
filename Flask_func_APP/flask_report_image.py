from flask import Flask, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
import os

image_bp = Blueprint('report_image', __name__)
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@image_bp.route('/report_image', methods=['POST'])
def report():
    try:
        user_id = request.form.get('user_id')
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        print(f"📥 신고 요청: user_id={user_id}, title={title}, content={content}")

        image_filename = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            image_filename = filename
            print(f"✅ 이미지 저장됨: {image_path}")
        else:
            print("⚠ 이미지 없음")

        # DB 저장 로직 추가 가능

        return jsonify({'message': '신고 완료'}), 201

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return jsonify({'error': str(e)}), 500
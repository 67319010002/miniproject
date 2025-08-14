from flask import Blueprint, request, jsonify, send_from_directory
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson import ObjectId
import os
from datetime import datetime

auth = Blueprint('auth', __name__)

# ตั้งค่าโฟลเดอร์สำหรับเก็บไฟล์
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route สำหรับแสดงรูปภาพ
@auth.route('/static/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@auth.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        email = request.form.get('email', '')
        password = request.form.get('password')
        profile_image = request.files.get('profile_image')

        if not username or not password:
            return jsonify({"msg": "Username and password required"}), 400

        if User.objects(username=username).first():
            return jsonify({"msg": "Username already exists"}), 400

        if email and User.objects(email=email).first():
            return jsonify({"msg": "Email already exists"}), 400

        hashed_pw = generate_password_hash(password)
        # บันทึกผู้ใช้ก่อนเพื่อได้ user.id
        user = User(
            username=username,
            email=email,
            password=hashed_pw
        ).save()

        profile_image_url = ""
        if profile_image:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # แก้ไขการสร้างชื่อไฟล์
            filename = secure_filename(f"{str(user.id)}_{timestamp}_{profile_image.filename}")
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            profile_image.save(save_path)
            profile_image_url = f"/static/uploads/{filename}"
            # อัปเดต URL รูปภาพในฐานข้อมูล
            user.profile_image_url = profile_image_url
            user.save()

        return jsonify({
            "msg": "User registered successfully",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "profile_image_url": user.profile_image_url
            }
        }), 201
    except Exception as e:
        return jsonify({"msg": f"Registration error: {str(e)}"}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"msg": "Username and password required"}), 400

        user = User.objects(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": token,
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "profile_image_url": user.profile_image_url or ""
            }
        }), 200
    except Exception as e:
        return jsonify({"msg": f"Login error: {str(e)}"}), 500

@auth.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404

        return jsonify({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "profile_image_url": user.profile_image_url or ""
        }), 200
    except Exception as e:
        return jsonify({"msg": f"Profile fetch error: {str(e)}"}), 500

@auth.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404

        username = request.form.get('username')
        email = request.form.get('email')
        profile_image = request.files.get('profile_image')

        # อัปเดต username
        # แก้ไขการตรวจสอบ: ตรวจสอบเฉพาะเมื่อ username มีการเปลี่ยนแปลง
        if username and username != user.username:
            if User.objects(username=username).first():
                return jsonify({"msg": "Username already exists"}), 400
            user.username = username

        # อัปเดต email
        # แก้ไขการตรวจสอบ: ตรวจสอบเฉพาะเมื่อ email มีการเปลี่ยนแปลง
        if email and email != user.email:
            if User.objects(email=email).first():
                return jsonify({"msg": "Email already exists"}), 400
            user.email = email

        # อัปเดตรูปภาพ
        if profile_image:
            # ลบไฟล์เก่าถ้ามี
            if user.profile_image_url and "static/uploads/" in user.profile_image_url:
                old_file = os.path.basename(user.profile_image_url)
                old_path = os.path.join(UPLOAD_FOLDER, old_file)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # สร้างชื่อไฟล์ใหม่
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # แก้ไขการสร้างชื่อไฟล์: ใช้ str(user.id)
            filename = secure_filename(f"{str(user.id)}_{timestamp}_{profile_image.filename}")
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            profile_image.save(save_path)
            user.profile_image_url = f"/static/uploads/{filename}"
        
        user.save()

        return jsonify({
            "msg": "Profile updated successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "profile_image_url": user.profile_image_url or ""
            }
        }), 200
    except Exception as e:
        return jsonify({"msg": f"Profile update error: {str(e)}"}), 500
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User, Comment
from bson import ObjectId

comments = Blueprint('comments', __name__)

# 🔹 API Endpoint สำหรับเพิ่มคอมเมนต์
# ต้อง login ก่อนถึงจะใช้งานได้
@comments.route('/<note_id>', methods=['POST'])
@jwt_required()
def add_comment(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    note = Note.objects(id=ObjectId(note_id)).first()

    if not note:
        return jsonify({"msg": "Note not found"}), 404

    data = request.get_json()
    content = data.get('content')

    if not content or len(content.strip()) == 0:
        return jsonify({"msg": "Comment content cannot be empty"}), 400

    comment = Comment(note=note, user=user, content=content)
    comment.save()

    return jsonify({
        "id": str(comment.id),
        "content": comment.content,
        "username": user.username,
        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 201

# 🔹 API Endpoint สำหรับดึงคอมเมนต์ของแต่ละโพสต์
@comments.route('/<note_id>', methods=['GET'])
def get_comments_for_note(note_id):
    note = Note.objects(id=ObjectId(note_id)).first()

    if not note:
        return jsonify({"msg": "Note not found"}), 404
        
    comments_list = Comment.objects(note=note).order_by('-created_at')

    return jsonify([
        {
            "id": str(comment.id),
            "content": comment.content,
            "username": comment.user.username,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for comment in comments_list
    ])
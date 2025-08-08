from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User, Favorite, Comment  # 🔹 เพิ่ม Comment เข้ามา
from mongoengine import Document, ReferenceField, ListField
from bson import ObjectId

notes = Blueprint('notes', __name__)

# --- Favorite Model ---
class Favorite(Document):
    user = ReferenceField(User, required=True, unique=True)
    notes = ListField(ReferenceField(Note))

# 🔹 ฟังก์ชันนับจำนวนคนที่แฟโวริทโน้ตแต่ละอัน (ปรับปรุงประสิทธิภาพ)
def count_favorites_for_notes(note_ids):
    if not note_ids:
        return {}
    
    pipeline = [
        {"$match": {"notes": {"$in": [ObjectId(note_id) for note_id in note_ids]}}},
        {"$unwind": "$notes"},
        {"$group": {"_id": "$notes", "count": {"$sum": 1}}}
    ]
    results = Favorite.objects.aggregate(pipeline)
    
    counts = {str(res['_id']): res['count'] for res in results}
    return counts

# 🔹 ฟังก์ชันช่วยสร้าง response data จากโน้ต (เพื่อลดความซ้ำซ้อน)
def create_note_response(note, favorite_counts):
    # 📌 ดึงจำนวนคอมเมนต์ของโน้ต
    comment_count = Comment.objects(note=note).count()

    return {
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "image_url": note.image_url or "",
        "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "username": note.user.username if note.user else "Unknown",
        "favorite_count": favorite_counts.get(str(note.id), 0),
        "comment_count": comment_count  # 📌 เพิ่มจำนวนคอมเมนต์
    }

# 🔹 Get all notes ของ user ปัจจุบัน
@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    all_notes = Note.objects(user=user).order_by('-created_at')
    
    note_ids = [str(note.id) for note in all_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([create_note_response(note, favorite_counts) for note in all_notes])

# 🔹 Create note ใหม่
@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=ObjectId(user_id)).first()

    note = Note(
        title=data.get('title'),
        content=data.get('content', ''),
        image_url=data.get('image_url', ''),
        user=user
    )
    
    if not note.title:
        return jsonify({"msg": "Title is required"}), 400
        
    note.save()
    return jsonify({"msg": "Note created!"})

# 🔹 Update note by ID
@notes.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    note = Note.objects(id=ObjectId(note_id), user=ObjectId(user_id)).first()
    
    if not note:
        return jsonify({"msg": "Note not found or you don't have permission to edit"}), 404

    data = request.get_json()
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    if 'image_url' in data:
        note.image_url = data['image_url']

    note.save()
    return jsonify({"msg": "Note updated!"})

# 🔹 Delete note by ID
@notes.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.objects(id=ObjectId(note_id), user=ObjectId(user_id)).first()
    
    if not note:
        return jsonify({"msg": "Note not found or you don't have permission to delete"}), 404
        
    # 📌 ลบคอมเมนต์ทั้งหมดที่เกี่ยวข้องกับโน้ตนี้
    Comment.objects(note=note).delete()

    note.delete()
    return jsonify({"msg": "Note deleted!"})

# 🔹 Search notes ของ user
@notes.route('/notes/search', methods=['GET'])
@jwt_required()
def search_notes():
    query = request.args.get('q', '').strip()
    user_id = get_jwt_identity()
    
    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    found_notes = Note.objects(
        user=ObjectId(user_id),
        __raw__={
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}}
            ]
        }
    ).order_by('-created_at')

    note_ids = [str(note.id) for note in found_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([create_note_response(note, favorite_counts) for note in found_notes])

# 🔹 Get all notes ของทุก user
@notes.route('/notes/all', methods=['GET'])
@jwt_required()
def get_all_notes():
    all_notes = Note.objects().order_by('-created_at')
    
    note_ids = [str(note.id) for note in all_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([create_note_response(note, favorite_counts) for note in all_notes])

# 🔹 Search notes ทุก user
@notes.route('/notes/all/search', methods=['GET'])
@jwt_required()
def search_all_notes():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    found_notes = Note.objects(
        __raw__={
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}}
            ]
        }
    ).order_by('-created_at')

    note_ids = [str(note.id) for note in found_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([create_note_response(note, favorite_counts) for note in found_notes])

# 🔹 Get favorite notes ของ user ปัจจุบัน
@notes.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    favorite = Favorite.objects(user=user).first()
    
    notes_list = []
    if favorite and favorite.notes:
        note_ids = [str(note.id) for note in favorite.notes]
        favorite_counts = count_favorites_for_notes(note_ids)

        notes_list = [create_note_response(note, favorite_counts) for note in favorite.notes]

    return jsonify(notes_list)

# 🔹 Toggle favorite note ของ user ปัจจุบัน
@notes.route('/favorites/<note_id>', methods=['POST'])
@jwt_required()
def toggle_favorite(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    favorite = Favorite.objects(user=user).first()
    note = Note.objects(id=ObjectId(note_id)).first()
    
    if not note:
        return jsonify({"msg": "Note not found"}), 404

    if not favorite:
        favorite = Favorite(user=user, notes=[])

    if note in favorite.notes:
        favorite.notes.remove(note)
    else:
        favorite.notes.append(note)

    favorite.save()
    return jsonify({"msg": "Favorite updated"})

# 🔹 Route สำหรับดึงคอมเมนต์ทั้งหมดของโน้ต
@notes.route("/comments/<note_id>", methods=["GET"])
def get_comments(note_id):
    try:
        note_oid = ObjectId(note_id)
        comments = Comment.objects(note=note_oid).order_by("-created_at")
        result = []
        for comment in comments:
            user = User.objects(id=comment.user.id).first()
            result.append({
                "id": str(comment.id),
                "content": comment.content,
                "username": user.username if user else "Unknown",
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
# 🔹 Route สำหรับเพิ่มคอมเมนต์ใหม่
@notes.route("/comments/<note_id>", methods=["POST"])
@jwt_required()
def add_comment(note_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=ObjectId(user_id)).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        note = Note.objects(id=ObjectId(note_id)).first()
        if not note:
            return jsonify({"error": "Note not found"}), 404
        
        data = request.get_json()
        content = data.get("content", "").strip()
        if not content:
            return jsonify({"error": "Comment content is required"}), 400
        
        # สร้างคอมเมนต์ใหม่ (ต้องส่งเป็น object reference ไม่ใช่แค่ ObjectId)
        new_comment = Comment(
            user=user,
            note=note,
            content=content
        )
        new_comment.save()

        # อัปเดตจำนวนคอมเมนต์ในโน้ต
        note.update(inc__comment_count=1)

        return jsonify({
            "id": str(new_comment.id),
            "content": new_comment.content,
            "username": user.username,
            "created_at": new_comment.created_at.strftime("%Y-%m-%d %H:%M")
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 🔹 Route สำหรับลบคอมเมนต์
@notes.route("/comments/<comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    try:
        # ดึง user id จาก JWT token
        user_id = get_jwt_identity()

        # หาคอมเมนต์ที่ต้องการลบ
        comment = Comment.objects(id=ObjectId(comment_id)).first()

        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # ตรวจสอบว่าผู้ใช้ที่กำลังลบคอมเมนต์เป็นเจ้าของคอมเมนต์นั้นหรือไม่
        if str(comment.user.id) != user_id:
            return jsonify({"error": "You do not have permission to delete this comment"}), 403

        # ลบคอมเมนต์
        comment.delete()

        # ลดจำนวนคอมเมนต์ในโน้ตที่เกี่ยวข้อง
        note = Note.objects(id=comment.note.id).first()
        if note:
            note.update(dec__comment_count=1)

        return jsonify({"message": "Comment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
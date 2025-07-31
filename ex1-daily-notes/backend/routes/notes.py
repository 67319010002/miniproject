from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User
from mongoengine import Document, ReferenceField, ListField
from bson import ObjectId

notes = Blueprint('notes', __name__)

# --- Favorite Model ---
class Favorite(Document):
    user = ReferenceField(User, required=True, unique=True)
    notes = ListField(ReferenceField(Note))

# ฟังก์ชันนับจำนวนคนที่แฟโวริทโน้ตแต่ละอัน
def count_favorites_for_notes(note_ids):
    counts = {}
    for note_id in note_ids:
        counts[note_id] = Favorite.objects(notes=ObjectId(note_id)).count()
    return counts

# 🔹 Get all notes ของ user ปัจจุบัน
@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    all_notes = Note.objects(user=user).order_by('-created_at')

    note_ids = [str(note.id) for note in all_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown",
            "favorite_count": favorite_counts.get(str(note.id), 0)
        }
        for note in all_notes
    ])

# 🔹 Create note ใหม่
@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=ObjectId(user_id)).first()

    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        image_url=data.get('image_url', ''),
        user=user
    )
    note.save()

    return jsonify({"msg": "Note created!"})

# 🔹 Update note by ID
@notes.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    data = request.get_json()
    update_data = {}

    if 'title' in data:
        update_data['title'] = data['title']
    if 'content' in data:
        update_data['content'] = data['content']
    if 'image_url' in data:
        update_data['image_url'] = data['image_url']

    Note.objects(id=ObjectId(note_id)).update_one(**update_data)
    return jsonify({"msg": "Note updated!"})

# 🔹 Delete note by ID
@notes.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    Note.objects(id=ObjectId(note_id)).delete()
    return jsonify({"msg": "Note deleted!"})

# 🔹 Search notes ของ user
@notes.route('/notes/search', methods=['GET'])
@jwt_required()
def search_notes():
    query = request.args.get('q', '').strip()
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    found_notes = Note.objects(
        user=user,
        __raw__={
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}}
            ]
        }
    ).order_by('-created_at')

    note_ids = [str(note.id) for note in found_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown",
            "favorite_count": favorite_counts.get(str(note.id), 0)
        }
        for note in found_notes
    ])

# 🔹 Get all notes ของทุก user
@notes.route('/notes/all', methods=['GET'])
@jwt_required()
def get_all_notes():
    all_notes = Note.objects().order_by('-created_at')

    note_ids = [str(note.id) for note in all_notes]
    favorite_counts = count_favorites_for_notes(note_ids)

    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown",
            "favorite_count": favorite_counts.get(str(note.id), 0)
        }
        for note in all_notes
    ])

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

    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown",
            "favorite_count": favorite_counts.get(str(note.id), 0)
        }
        for note in found_notes
    ])

# 🔹 Get favorite notes ของ user ปัจจุบัน
@notes.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    favorite = Favorite.objects(user=user).first()

    notes_list = []
    if favorite:
        note_ids = [str(note.id) for note in favorite.notes]
        favorite_counts = count_favorites_for_notes(note_ids)

        notes_list = [
            {
                "id": str(note.id),
                "title": note.title,
                "content": note.content,
                "image_url": note.image_url or "",
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "username": note.user.username if note.user else "Unknown",
                "favorite_count": favorite_counts.get(str(note.id), 0)
            }
            for note in favorite.notes
        ]

    return jsonify(notes_list)

# 🔹 Toggle favorite note ของ user ปัจจุบัน
@notes.route('/favorites/<note_id>', methods=['POST'])
@jwt_required()
def toggle_favorite(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    favorite = Favorite.objects(user=user).first()
    note = Note.objects(id=ObjectId(note_id)).first()
    if not note:
        return jsonify({"msg": "Note not found"}), 404

    if not favorite:
        favorite = Favorite(user=user, notes=[])

    # เช็คด้วย id เท่านั้น
    if any(str(n.id) == str(note.id) for n in favorite.notes):
        favorite.notes = [n for n in favorite.notes if str(n.id) != str(note.id)]
    else:
        favorite.notes.append(note)

    favorite.save()
    return jsonify({"msg": "Favorite updated"})

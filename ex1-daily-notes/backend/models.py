from mongoengine import Document, StringField, ReferenceField, DateTimeField, CASCADE, ListField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)        # ชื่อผู้ใช้ ห้ามซ้ำ
    email = StringField(required=False, unique=True)           # อีเมล (optional) เพิ่ม unique ได้ถ้าต้องการ
    password = StringField(required=True)                     # รหัสผ่าน (hash แล้ว)
    profile_image_url = StringField(default=None)             # URL รูปโปรไฟล์ (optional)

class Note(Document):
    title = StringField(required=True)
    content = StringField(default='')
    image_url = StringField(default=None)
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    # 📌 เพิ่ม field สำหรับเก็บ comments
    comments = ListField(ReferenceField('Comment'))


class Favorite(Document):
    user = ReferenceField(User, required=True, unique=True, reverse_delete_rule=CASCADE)  # ผู้ใช้ที่เก็บรายการโน้ตที่ชอบ (แยกตามคน)
    notes = ListField(ReferenceField(Note), default=list)  # รายการโน้ตที่ถูกกด Favorite

class Comment(Document):
    note = ReferenceField('Note', reverse_delete_rule=CASCADE, required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    content = StringField(required=True, max_length=500)
    created_at = DateTimeField(default=datetime.utcnow)
from mongoengine import Document, StringField, ReferenceField, DateTimeField, CASCADE, ListField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)        # ชื่อผู้ใช้ ห้ามซ้ำ
    password = StringField(required=True)                     # รหัสผ่าน (hash แล้ว)
    profile_image_url = StringField(default=None)             # URL รูปโปรไฟล์ (optional)

class Note(Document):
    title = StringField(required=True)                         # หัวข้อโน้ต
    content = StringField(default='')                          # เนื้อหาโน้ต
    image_url = StringField(default=None)                      # URL รูปภาพในโน้ต (optional)
    created_at = DateTimeField(default=datetime.utcnow)        # วันที่สร้าง (อัตโนมัติ)
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)  # เจ้าของโน้ต

class Favorite(Document):
    user = ReferenceField(User, required=True, unique=True, reverse_delete_rule=CASCADE)  # ผู้ใช้ที่เก็บรายการโน้ตที่ชอบ (แยกตามคน)
    notes = ListField(ReferenceField(Note), default=list)  # รายการโน้ตที่ถูกกด Favorite

<template>
  <div class="min-h-screen bg-black text-white p-6 max-w-6xl mx-auto grid grid-cols-10 gap-8">
    <!-- All Notes (ซ้าย 70%) -->
    <div class="col-span-7">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold">📚 All Notes</h1>
        <button
          @click="fetchAllNotes"
          class="btn-black text-sm px-3 py-1 hover:bg-gray-700"
          title="Refresh All Notes"
        >
          🔄 Refresh
        </button>
      </div>
      <input
        v-model="searchAllQuery"
        placeholder="Search all notes..."
        class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md w-full mb-4 focus:outline-none focus:ring focus:ring-blue-500"
        @input="debouncedSearchAll"
      />

      <div v-if="allNotes.length > 0" class="space-y-4">
        <div
          v-for="note in allNotes"
          :key="note.id"
          class="bg-gray-900 border border-gray-700 p-4 rounded-md relative group cursor-pointer note-hover-effect"
          @click="openNoteModal(note)"
        >
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold">{{ note.title }}</h2>
          </div>

          <p class="text-gray-300 mt-2">{{ note.content }}</p>

          <!-- รูปภาพถ้ามี -->
          <div v-if="note.image_url" class="mt-4 mb-0">
            <img
              :src="note.image_url"
              alt="Note Image"
              class="w-full max-h-48 object-contain rounded"
            />
          </div>

          <div
            class="absolute bottom-2 right-2 bg-gray-800 text-xs text-gray-300 px-2 py-1 rounded select-none z-10"
            style="white-space: nowrap;"
          >
            Written by: <span class="font-semibold">{{ note.username || 'Unknown' }}</span>
          </div>
        </div>
      </div>
      <div v-else class="text-gray-500 mt-8">No notes to display</div>
    </div>

    <!-- My Notes (ขวา 30%) -->
    <div class="col-span-3">

      <!-- แก้ไขโปรไฟล์แบบ Dropdown ตอน Hover -->
      <div
        class="relative flex items-center bg-gray-700 rounded-md p-3 mb-4 max-w-full space-x-4 cursor-pointer group"
        title="Hover to edit profile"
      >
        <img
          :src="userAvatar"
          alt="User Avatar"
          class="w-12 h-12 rounded-full object-cover flex-shrink-0"
        />
        <span class="text-white font-semibold text-lg truncate">{{ userName }}</span>

        <!-- ไอคอนฟันเฟืองเล็ก -->
        <div
          class="ml-auto text-white text-lg px-2 py-1 rounded hover:bg-gray-600"
          title="Edit Profile"
        >
          ⚙️
        </div>

        <!-- เมนูแก้ไขโปรไฟล์ แสดงตอน hover -->
        <div
          class="absolute right-0 top-full mt-2 bg-gray-800 p-4 rounded-md shadow-lg w-64 opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity duration-300 z-20"
        >
          <input
            v-model="editUserName"
            placeholder="Edit username"
            class="w-full p-2 rounded border border-gray-600 bg-gray-900 text-white focus:outline-none focus:ring focus:ring-blue-500 mb-2"
          />

          <input
            type="file"
            accept="image/*"
            @change="onAvatarFileChange"
            class="w-full p-2 rounded border border-gray-600 bg-gray-900 text-white focus:outline-none focus:ring focus:ring-blue-500 mb-2"
          />

          <img
            v-if="editUserAvatar && !userAvatarError"
            :src="editUserAvatar"
            alt="Avatar preview"
            class="w-20 h-20 object-cover rounded-full mx-auto mb-2"
            @error="userAvatarError = true"
            @load="userAvatarError = false"
          />
          <span v-if="userAvatarError" class="text-red-500 block mb-2 text-center">
            รูปภาพไม่ถูกต้องหรือโหลดไม่สำเร็จ
          </span>

          <div class="flex space-x-2">
            <button @click="saveUserProfile" class="btn-black flex-1">💾 Save</button>
            <button @click="cancelEditUser" class="btn-black flex-1">✖️ Cancel</button>
          </div>
        </div>
      </div>

      <h1 class="text-3xl font-bold mb-6">📝 My Notes</h1>

      <!-- Create Note -->
      <div class="flex gap-2 mb-2">
        <input
          v-model="title"
          placeholder="Title"
          class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md w-1/4 focus:outline-none focus:ring focus:ring-blue-500"
        />
        <input
          v-model="content"
          placeholder="Content"
          class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md flex-1 focus:outline-none focus:ring focus:ring-blue-500"
        />
      </div>
      <div class="mb-4 flex items-center">
        <input
          v-model="imageUrl"
          placeholder="Image URL"
          class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md w-full focus:outline-none focus:ring focus:ring-blue-500"
        />
        <img
          v-if="imageUrl && !imagePreviewError"
          :src="imageUrl"
          alt="Preview Image"
          class="inline-block ml-2 w-16 max-h-12 object-contain rounded"
          @error="imagePreviewError = true"
          @load="imagePreviewError = false"
        />
        <span
          v-if="imagePreviewError"
          class="text-red-500 ml-2"
        >URL รูปภาพไม่ถูกต้อง</span>
      </div>
      <button
        @click="createNote"
        class="bg-green-600 hover:bg-green-700 text-white p-2 rounded-md w-full mb-6"
      >
        Add
      </button>

      <input
        v-model="searchMyQuery"
        placeholder="Search my notes..."
        class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md w-full mb-4 focus:outline-none focus:ring focus:ring-blue-500"
        @input="debouncedSearchMy"
      />

      <div v-if="myNotes.length > 0" class="space-y-4">
        <div
          v-for="note in myNotes"
          :key="note.id"
          class="bg-gray-900 border border-gray-700 p-4 rounded-md relative group"
        >
          <div class="flex justify-between items-center mb-2">
            <h2 v-if="editNoteId !== note.id" class="text-xl font-semibold">{{ note.title }}</h2>

            <div class="flex space-x-2 items-center">
              <!-- ถ้าอยู่ในโหมดแก้ไขแสดงปุ่ม Save, Cancel -->
              <button
                v-if="editNoteId === note.id"
                @click="saveNote(note.id)"
                class="btn-black"
                title="Save"
              >
                💾
              </button>
              <button
                v-if="editNoteId === note.id"
                @click="cancelEdit"
                class="btn-black"
                title="Cancel"
              >
                ✖️
              </button>

              <!-- ถ้าไม่ใช่โหมดแก้ไข แสดงไอคอนปากกาแก้ไข + ถังขยะลบ -->
              <template v-else>
                <button
                  @click="startEdit(note)"
                  class="btn-black"
                  title="Edit"
                >
                  ✏️
                </button>
                <button
                  @click="deleteNote(note.id)"
                  class="btn-black text-red-500 hover:text-red-600"
                  title="Delete"
                >
                  🗑️
                </button>
              </template>
            </div>
          </div>

          <!-- input title + image URL ย้ายไปไว้ข้างล่างปุ่ม -->
          <div v-if="editNoteId === note.id" class="mb-2 space-y-2">
            <input
              v-model="editTitle"
              class="bg-gray-800 text-white border border-gray-600 p-1 rounded w-full"
              placeholder="Title"
            />
            <input
              v-model="editImageUrl"
              class="bg-gray-800 text-white border border-gray-600 p-1 rounded w-full"
              placeholder="Image URL"
            />
          </div>

          <textarea
            v-if="editNoteId === note.id"
            v-model="editContent"
            class="bg-gray-800 text-white border border-gray-600 p-2 rounded w-full"
            rows="3"
          ></textarea>

          <div v-else>
            <p class="text-gray-300 mt-2">{{ note.content }}</p>
            <div v-if="note.image_url" class="mt-2">
              <img
                :src="note.image_url"
                alt="Note Image"
                class="w-full max-h-40 object-contain rounded"
              />
            </div>
          </div>

          <div
            class="absolute bottom-2 right-2 bg-gray-800 text-xs text-gray-300 px-2 py-1 rounded select-none z-10"
            style="white-space: nowrap;"
          >
            Written by: <span class="font-semibold">{{ note.username || 'Unknown' }}</span>
          </div>
        </div>
      </div>
      <div v-else class="text-gray-500 mt-8">No notes to display</div>
    </div>

    <!-- Modal Popup for Selected Note -->
    <div
      v-if="selectedNote"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeNoteModal"
      style="background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);"
    >
      <div class="bg-gray-900 p-6 rounded-md max-w-lg w-full shadow-lg relative">
        <button
          @click="closeNoteModal"
          class="absolute top-2 right-2 text-gray-400 hover:text-white text-xl font-bold"
          aria-label="Close modal"
        >
          &times;
        </button>

        <!-- Title และ Content อยู่บนรูป -->
        <h2 class="text-2xl font-bold mb-2">{{ selectedNote.title }}</h2>
        <p class="whitespace-pre-wrap text-gray-300 mb-4">{{ selectedNote.content }}</p>

        <div v-if="selectedNote.image_url" class="mt-2">
          <img
            :src="selectedNote.image_url"
            alt="Note Image"
            class="w-full max-h-60 object-contain rounded"
          />
        </div>

        <div class="text-xs text-gray-400 mt-4">
          Written by: <span class="font-semibold">{{ selectedNote.username || 'Unknown' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const title = ref('')
const content = ref('')
const imageUrl = ref('')
const imagePreviewError = ref(false) // สำหรับตรวจสอบรูปพรีวิว

const myNotes = ref([])
const allNotes = ref([])
const searchMyQuery = ref('')
const searchAllQuery = ref('')
const token = localStorage.getItem('token')

// ตัวแปรแสดงชื่อยูสเซอร์และรูป (ตัวอย่าง)
const userName = ref('Chanid')
// เปลี่ยนให้ userAvatar เริ่มต้นเป็นค่าว่าง (ถ้าไม่มีรูปเก็บใน localStorage)
const userAvatar = ref(localStorage.getItem('userAvatar') || 'https://i.pravatar.cc/40')

// ตัวแปรแก้ไขโปรไฟล์
const editUserName = ref(userName.value)
const editUserAvatar = ref(userAvatar.value) // จะเก็บ data URL ของไฟล์
const userAvatarError = ref(false)

const editNoteId = ref(null)
const editTitle = ref('')
const editContent = ref('')
const editImageUrl = ref('')

const selectedNote = ref(null)
const openNoteModal = (note) => {
  selectedNote.value = note
}
const closeNoteModal = () => {
  selectedNote.value = null
}

const fetchMyNotes = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/notes', {
      headers: { Authorization: `Bearer ${token}` },
    })
    myNotes.value = res.data
  } catch (e) {
    console.error('Failed to fetch my notes:', e)
  }
}

const fetchAllNotes = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/notes/all', {
      headers: { Authorization: `Bearer ${token}` },
    })
    allNotes.value = res.data
  } catch (e) {
    console.error('Failed to fetch all notes:', e)
  }
}

const createNote = async () => {
  if (!title.value || !content.value) return
  try {
    await axios.post(
      'http://localhost:5000/api/notes',
      { title: title.value, content: content.value, image_url: imageUrl.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    title.value = ''
    content.value = ''
    imageUrl.value = ''
    imagePreviewError.value = false
    fetchMyNotes()
  } catch (e) {
    console.error('Failed to create note:', e)
  }
}

const deleteNote = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/api/notes/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    fetchMyNotes()
  } catch (e) {
    console.error('Failed to delete note:', e)
  }
}

const startEdit = (note) => {
  editNoteId.value = note.id
  editTitle.value = note.title
  editContent.value = note.content
  editImageUrl.value = note.image_url || ''
}

const cancelEdit = () => {
  editNoteId.value = null
  editTitle.value = ''
  editContent.value = ''
  editImageUrl.value = ''
}

const saveNote = async (id) => {
  try {
    await axios.put(
      `http://localhost:5000/api/notes/${id}`,
      { title: editTitle.value, content: editContent.value, image_url: editImageUrl.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    cancelEdit()
    fetchMyNotes()
  } catch (e) {
    console.error('Failed to save note:', e)
  }
}

const searchMyNotes = async () => {
  const q = searchMyQuery.value.trim()
  if (!q) return fetchMyNotes()
  try {
    const res = await axios.get(`http://localhost:5000/api/notes/search?q=${encodeURIComponent(q)}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    myNotes.value = res.data
  } catch (e) {
    console.error('Failed to search my notes:', e)
  }
}

const searchAllNotes = async () => {
  const q = searchAllQuery.value.trim()
  if (!q) return fetchAllNotes()
  try {
    const res = await axios.get(`http://localhost:5000/api/notes/all/search?q=${encodeURIComponent(q)}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    allNotes.value = res.data
  } catch (e) {
    console.error('Failed to search all notes:', e)
  }
}

let timeoutMy
const debouncedSearchMy = () => {
  clearTimeout(timeoutMy)
  timeoutMy = setTimeout(() => {
    searchMyNotes()
  }, 300)
}

let timeoutAll
const debouncedSearchAll = () => {
  clearTimeout(timeoutAll)
  timeoutAll = setTimeout(() => {
    searchAllNotes()
  }, 300)
}

// ฟังก์ชันจัดการเมื่อเลือกไฟล์อวาตาร์
const onAvatarFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    userAvatarError.value = true
    return
  }

  userAvatarError.value = false

  const reader = new FileReader()
  reader.onload = (e) => {
    editUserAvatar.value = e.target.result
  }
  reader.onerror = () => {
    userAvatarError.value = true
  }
  reader.readAsDataURL(file)
}

const saveUserProfile = async () => {
  if (!editUserName.value.trim()) {
    alert('กรุณากรอกชื่อผู้ใช้')
    return
  }
  if (userAvatarError.value) {
    alert('รูปภาพไม่ถูกต้องหรือโหลดไม่สำเร็จ')
    return
  }

  userName.value = editUserName.value.trim()
  userAvatar.value = editUserAvatar.value

  // บันทึกลง localStorage
  localStorage.setItem('userAvatar', editUserAvatar.value)
  localStorage.setItem('userName', userName.value)

  // ปิดเมนูแก้ไข
  // (ถ้าอยากให้ปิดตอน save ต้องซ่อนเมนูด้วยการจัดการ state หรือ event)
  // ในที่นี้เพราะเมนูเป็น hover-based จะซ่อนเองเมื่อเอาเมาส์ออก
}

const cancelEditUser = () => {
  editUserName.value = userName.value
  editUserAvatar.value = userAvatar.value
  userAvatarError.value = false
}

onMounted(() => {
  // โหลด userName จาก localStorage ถ้ามี
  const storedName = localStorage.getItem('userName')
  if (storedName) {
    userName.value = storedName
    editUserName.value = storedName
  }

  fetchMyNotes()
  fetchAllNotes()
})
</script>

<style>
html,
body {
  background-color: #000;
}

/* ปุ่มสีดำ มุมมน พร้อม transition และโฮเวอร์ */
.btn-black {
  background-color: #000;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid transparent;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  user-select: none;
}

.btn-black:hover {
  background-color: #222;
  color: #a3a3a3;
  border-color: #555;
}

.btn-black.text-red-500 {
  background-color: transparent;
  border: none;
  padding: 0;
  font-size: 1.125rem;
  line-height: 1;
}

.note-hover-effect {
  transition: all 0.3s ease; /* ใส่ transition ให้ smooth */
}

.note-hover-effect:hover {
  border-color: #fff; /* ขอบสีขาว */
  box-shadow: 0 6px 12px rgba(255, 255, 255, 0.7); /* แสงสีขาว */
  transform: translateY(-6px); /* เด้งขึ้น 6px */
}

textarea {
  resize: vertical;
  min-height: 80px;
}
</style>

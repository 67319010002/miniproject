<template>
  <div class="min-h-screen bg-black text-white p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 flex items-center gap-3">
      ❤️ Favorite Notes
      <button @click="refreshFavorites" class="btn-black text-sm px-3 py-1 hover:bg-gray-700">
        🔄 Refresh
      </button>
    </h1>

    <div v-if="favoriteNotesList.length > 0" class="space-y-4">
      <div
        v-for="note in favoriteNotesList"
        :key="note.id"
        class="bg-gray-800 border border-gray-600 p-4 rounded-md cursor-pointer note-hover-effect flex items-center gap-4 relative"
        @click="openNoteModal(note)"
      >
        <div class="w-16 h-16 flex-shrink-0 bg-gray-700 rounded overflow-hidden">
          <img
            v-if="note.image_url"
            :src="note.image_url"
            alt="Note Image"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-gray-500 text-sm">
            No Image
          </div>
        </div>

        <div class="flex-1 min-w-0">
          <h3 class="font-semibold text-lg mb-1 truncate">{{ note.title }}</h3>
          <p class="text-gray-400 text-sm truncate">{{ note.content }}</p>
        </div>

        <button
          @click.stop="removeFavorite(note.id)"
          class="text-gray-400 hover:text-red-500 absolute top-2 right-2 p-1"
          aria-label="Remove from favorites"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm6 0a1 1 0 112 0v6a1 1 0 11-2 0V8z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>

    <div v-else class="text-gray-500 text-center mt-20 text-lg">
      No favorite notes yet.
    </div>

    <div
  v-if="selectedNote"
  class="fixed inset-0 flex items-center justify-center z-50"
  @click.self="closeNoteModal"
  style="background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);"
>
  <div class="bg-white p-6 rounded-md max-w-lg w-full shadow-lg relative">
    <button
      @click="closeNoteModal"
      class="absolute top-2 right-2 text-gray-700 hover:text-black text-xl font-bold"
      aria-label="Close modal"
    >
      &times;
    </button>
    <h2 class="text-2xl font-bold mb-2 text-black">{{ selectedNote.title }}</h2>
    <p class="whitespace-pre-wrap text-gray-900 mb-4">{{ selectedNote.content }}</p>
    <div v-if="selectedNote.image_url" class="mt-2">
      <img
        :src="selectedNote.image_url"
        alt="Note Image"
        class="w-full max-h-60 object-contain rounded"
      />
    </div>
    <div class="text-xs text-gray-700 mt-4">
      Written by: <span class="font-semibold">{{ selectedNote.username || 'Unknown' }}</span>
    </div>

    <div class="mt-6 border-t border-gray-200 pt-4 text-black">
      <h3 class="text-xl font-semibold mb-4">Comments ({{ noteComments.length }})</h3>
      <div class="space-y-4 max-h-60 overflow-y-auto pr-2">
        <div v-if="noteComments.length > 0">
          <div v-for="comment in noteComments" :key="comment.id" class="p-3 bg-gray-100 rounded-md">
            <div class="flex items-center text-sm font-semibold text-gray-800">
              <span class="text-xs text-gray-500 mr-2">{{ comment.created_at }}</span>
              {{ comment.username }}
            </div>
            <p class="mt-1 text-gray-700">{{ comment.content }}</p>
          </div>
        </div>
        <div v-else class="text-gray-500 text-center">No comments yet.</div>
      </div>
      <form @submit.prevent="submitComment" class="mt-4">
        <textarea
          v-model="newCommentContent"
          placeholder="Write a comment..."
          class="w-full p-2 text-sm text-gray-900 bg-gray-100 rounded-md focus:outline-none focus:ring focus:ring-blue-500"
          rows="2"
        ></textarea>
        <button
          type="submit"
          class="mt-2 w-full bg-blue-500 text-white hover:bg-blue-600 rounded text-sm px-3 py-1"
        >
          Post Comment
        </button>
      </form>
    </div>
  </div>
</div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

const token = localStorage.getItem('token')
const allNotes = ref([])
const favoriteNoteIds = ref(new Set())

const selectedNote = ref(null)
// 🔹 เพิ่มตัวแปรสำหรับคอมเมนต์
const newCommentContent = ref('')
const noteComments = ref([])

// 🔹 ปรับปรุงฟังก์ชัน openNoteModal ให้ดึงคอมเมนต์มาแสดง
const openNoteModal = (note) => {
  selectedNote.value = note
  if (note && note.id) {
    fetchComments(note.id)
  }
}

// 🔹 ปรับปรุงฟังก์ชัน closeNoteModal ให้ล้างข้อมูลคอมเมนต์
const closeNoteModal = () => {
  selectedNote.value = null
  noteComments.value = []
  newCommentContent.value = ''
}

// 🔹 ฟังก์ชันสำหรับดึงคอมเมนต์จาก Backend
const fetchComments = async (noteId) => {
  try {
    const res = await axios.get(`http://localhost:5000/api/comments/${noteId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    noteComments.value = res.data
  } catch (e) {
    console.error('Failed to fetch comments:', e)
  }
}

// 🔹 ฟังก์ชันสำหรับส่งคอมเมนต์ใหม่
const submitComment = async () => {
  if (!newCommentContent.value.trim()) return

  try {
    const res = await axios.post(
      `http://localhost:5000/api/comments/${selectedNote.value.id}`,
      { content: newCommentContent.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    noteComments.value.unshift(res.data)
    newCommentContent.value = ''
    
    // อัปเดตจำนวนคอมเมนต์บนโน้ตที่เลือก
    if (selectedNote.value) {
      selectedNote.value.comment_count = noteComments.value.length
    }
  } catch (e) {
    console.error('Failed to post comment:', e)
  }
}

// ... โค้ดเดิมส่วนอื่นๆ
const fetchFavoritesFromBackend = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/favorites', {
      headers: { Authorization: `Bearer ${token}` },
    })
    // เก็บเฉพาะ ID ของโน้ตที่ชื่นชอบ
    favoriteNoteIds.value = new Set(res.data.map(note => note.id))
  } catch (e) {
    console.error('Failed to fetch favorite notes:', e)
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

const toggleFavorite = async (noteId) => {
  try {
    await axios.post(
      `http://localhost:5000/api/favorites/${noteId}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    // อัปเดตรายการ favorite ใน Vue.js หลังจาก API สำเร็จ
    if (favoriteNoteIds.value.has(noteId)) {
      favoriteNoteIds.value.delete(noteId);
    } else {
      favoriteNoteIds.value.add(noteId);
    }
  } catch (e) {
    console.error('Failed to toggle favorite:', e);
  }
};

const favoriteNotesList = computed(() => {
  return allNotes.value.filter(note => favoriteNoteIds.value.has(note.id))
})

const refreshFavorites = () => {
  fetchFavoritesFromBackend()
  fetchAllNotes()
}

onMounted(() => {
  fetchFavoritesFromBackend()
  fetchAllNotes()
})
</script>

<style>
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

.note-hover-effect {
  transition: all 0.3s ease;
}

.note-hover-effect:hover {
  border-color: #fff;
  box-shadow: 0 6px 12px rgba(255, 255, 255, 0.7);
  transform: translateY(-6px);
}
</style>
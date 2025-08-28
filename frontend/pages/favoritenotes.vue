<template>
  <div class="min-h-screen bg-black text-white p-6 max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 flex items-center gap-3">
      ❤️ Favorite Notes
      <button @click="refreshFavorites" class="btn-black text-sm px-3 py-1 hover:bg-gray-700">
        🔄 Refresh
      </button>
    </h1>

    <!-- Grid แสดงการ์ด -->
    <div v-if="favoriteNotesList.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
      <div
        v-for="note in favoriteNotesList"
        :key="note.id"
        class="group relative bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl border border-gray-700 overflow-hidden shadow-md hover:shadow-2xl transition-all duration-300 cursor-pointer flex flex-col"
        @click="openNoteModal(note)"
      >
        <!-- ปุ่มลบ favorite -->
        <button
          @click.stop="removeFavorite(note.id)"
          class="absolute top-3 right-3 bg-black/60 backdrop-blur-sm p-2 rounded-full text-gray-400 hover:text-red-500 hover:scale-110 transition-all duration-200 z-10"
        >
          ✖
        </button>

        <!-- รูป -->
        <div class="h-36 w-full overflow-hidden relative">
          <img
            v-if="note.image_url"
            :src="note.image_url"
            alt="Note Image"
            class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          />
          <div v-else class="h-full flex items-center justify-center bg-gray-800 text-gray-500 text-sm">
            No Image
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent"></div>
        </div>

        <!-- เนื้อหา -->
        <div class="p-4 flex flex-col flex-1">
          <h3 class="font-bold text-base mb-1 text-white line-clamp-1 group-hover:text-blue-400 transition-colors duration-300">
            {{ note.title }}
          </h3>
          <p class="text-gray-400 text-xs flex-grow line-clamp-2">
            {{ note.content }}
          </p>

          <!-- Stats -->
          <div class="flex justify-between items-center text-xs text-gray-400 mt-3 border-t border-gray-700 pt-2">
            <span class="flex items-center gap-1">
              ❤️ <span class="font-medium">{{ note.favorite_count || 0 }}</span>
            </span>
            <span class="flex items-center gap-1">
              💬 <span class="font-medium">{{ note.comment_count || 0 }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- ถ้าไม่มี -->
    <div v-else class="text-gray-500 text-center mt-20 text-lg">
      No favorite notes yet.
    </div>

    <!-- Modal -->
    <div
      v-if="selectedNote"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeNoteModal"
      style="background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(8px);"
    >
      <div class="bg-white p-6 rounded-md shadow-lg relative flex w-[750px] h-[500px] overflow-hidden">
        <button
          @click="closeNoteModal"
          class="absolute top-2 right-2 text-gray-700 hover:text-black text-xl font-bold"
        >
          &times;
        </button>

        <!-- เนื้อหา -->
        <div class="flex-1 pr-4 overflow-y-auto">
          <div class="flex items-center gap-2 mb-2">
            <img
              v-if="selectedNote.user_profile_pic"
              :src="getFullProfilePicURL(selectedNote.user_profile_pic)"
              class="w-8 h-8 rounded-full object-cover"
            />
            <div
              v-else
              class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-white font-bold text-sm"
            >
              {{ selectedNote.username ? selectedNote.username.charAt(0).toUpperCase() : "?" }}
            </div>
            <span class="font-semibold text-black">{{ selectedNote.username || "Unknown" }}</span>
          </div>

          <h2 class="text-2xl font-bold mb-2 text-black">{{ selectedNote.title }}</h2>
          <p class="text-gray-900 mb-4 whitespace-pre-wrap max-h-24 overflow-y-auto">
            {{ selectedNote.content }}
          </p>

          <img
            v-if="selectedNote.image_url"
            :src="selectedNote.image_url"
            class="w-full max-h-60 object-contain rounded"
          />

          <!-- remove fav -->
          <button
            @click.stop="removeFavorite(selectedNote.id)"
            class="absolute left-3 bottom-3 text-2xl cursor-pointer"
          >
            <span class="text-red-500">❤️</span>
          </button>
        </div>

        <!-- คอมเมนต์ -->
        <div class="flex-1 border-l pl-4 flex flex-col">
          <h3 class="text-xl font-semibold mb-2">
            Comments ({{ noteComments.length }})
          </h3>
          <div class="flex-grow overflow-y-auto pr-2 space-y-2">
            <div
              v-for="comment in noteComments"
              :key="comment.id"
              class="p-3 bg-gray-100 rounded-md"
            >
              <div class="flex justify-between text-sm font-semibold text-gray-800">
                {{ comment.username }}
                <button
                  v-if="comment.username === username"
                  @click="deleteComment(comment.id, selectedNote.id)"
                  class="text-red-500 hover:text-red-700 text-xs"
                >
                  &times; Delete
                </button>
              </div>
              <p class="text-gray-700">{{ comment.content }}</p>
              <div class="text-right text-xs text-gray-500">
                {{ comment.created_at }}
              </div>
            </div>
            <div v-if="noteComments.length === 0" class="text-gray-400 text-center">
              No comments yet.
            </div>
          </div>

          <form @submit.prevent="submitComment" class="mt-2">
            <textarea
              v-model="newCommentContent"
              rows="2"
              placeholder="Write a comment..."
              class="w-full p-2 text-sm text-gray-900 bg-gray-100 rounded-md focus:ring focus:ring-blue-500"
            ></textarea>
            <button
              type="submit"
              class="mt-2 w-full bg-blue-500 text-white hover:bg-blue-600 rounded px-3 py-1 text-sm"
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
import axios from "axios"
import { ref, computed, onMounted } from "vue"

const token = localStorage.getItem("token")
const username = ref(localStorage.getItem("username") || "guest")
const allNotes = ref([])
const favoriteNoteIds = ref(new Set())
const selectedNote = ref(null)
const newCommentContent = ref("")
const noteComments = ref([])
const backendBaseURL = import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:5000";

const fetchFavoritesFromBackend = async () => {
  try {
    const res = await axios.get(`${backendBaseURL}/api/favorites`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    favoriteNoteIds.value = new Set(res.data.map((n) => n.id))
  } catch (e) {
    console.error("Failed to fetch favorites:", e)
  }
}

const fetchAllNotes = async () => {
  try {
    const res = await axios.get(`${backendBaseURL}/api/notes/all`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    allNotes.value = res.data
  } catch (e) {
    console.error("Failed to fetch notes:", e)
  }
}

const favoriteNotesList = computed(() =>
  allNotes.value.filter((n) => favoriteNoteIds.value.has(n.id))
)

const refreshFavorites = () => {
  fetchFavoritesFromBackend()
  fetchAllNotes()
}

const openNoteModal = (note) => {
  selectedNote.value = note
  if (note?.id) fetchComments(note.id)
}

const closeNoteModal = () => {
  selectedNote.value = null
  noteComments.value = []
  newCommentContent.value = ""
}

const fetchComments = async (noteId) => {
  try {
    const res = await axios.get(`${backendBaseURL}/api/comments/${noteId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    noteComments.value = res.data
  } catch (e) {
    console.error("Failed to fetch comments:", e)
  }
}

const submitComment = async () => {
  if (!newCommentContent.value.trim()) return
  try {
    const res = await axios.post(
      `${backendBaseURL}/api/comments/${selectedNote.value.id}`,
      { content: newCommentContent.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    noteComments.value.unshift(res.data)
    newCommentContent.value = ""
    if (selectedNote.value)
      selectedNote.value.comment_count = noteComments.value.length
  } catch (e) {
    console.error("Failed to post comment:", e)
  }
}

const deleteComment = async (commentId, noteId) => {
  if (!confirm("Delete this comment?")) return
  try {
    await axios.delete(`${backendBaseURL}/api/comments/${commentId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    noteComments.value = noteComments.value.filter((c) => c.id !== commentId)
    const n = allNotes.value.find((n) => n.id === noteId)
    if (n) n.comment_count = noteComments.value.length
    if (selectedNote.value) selectedNote.value.comment_count = noteComments.value.length
  } catch (e) {
    console.error("Failed to delete comment:", e)
  }
}

const removeFavorite = async (noteId) => {
  try {
    await axios.post(`${backendBaseURL}/api/favorites/${noteId}`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    })
    favoriteNoteIds.value.delete(noteId)
    const note = allNotes.value.find((n) => n.id === noteId)
    if (note) note.favorite_count = (note.favorite_count || 1) - 1
    if (selectedNote.value?.id === noteId)
      selectedNote.value.favorite_count = (selectedNote.value.favorite_count || 1) - 1
  } catch (e) {
    console.error("Failed to remove favorite:", e)
  }
}

const getFullProfilePicURL = (path) => {
  if (!path) return ""
  if (path.startsWith("http")) return path
  return `${backendBaseURL}${path}`
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
  transition: 0.3s;
}
.btn-black:hover {
  background-color: #222;
  color: #a3a3a3;
  border-color: #555;
}
</style>

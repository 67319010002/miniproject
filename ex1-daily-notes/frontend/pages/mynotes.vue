<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white p-6 max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">📝 My Notes</h1>

    <!-- Create Note -->
    <div class="flex gap-2 mb-2">
      <input
        v-model="title"
        placeholder="Title"
        class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md w-1/4 focus:outline-none focus:ring focus:ring-blue-500 shadow-sm"
      />
      <input
        v-model="content"
        placeholder="Content"
        class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md flex-1 focus:outline-none focus:ring focus:ring-blue-500 shadow-sm"
      />
    </div>
    <div class="mb-4 flex items-center">
      <input
        v-model="imageUrl"
        placeholder="Image URL"
        class="bg-gray-800 text-white border border-gray-700 p-2 rounded-md w-full focus:outline-none focus:ring focus:ring-blue-500 shadow-sm"
      />
      <img
        v-if="imageUrl && !imagePreviewError"
        :src="imageUrl"
        alt="Preview"
        class="inline-block ml-2 w-16 max-h-12 object-contain rounded"
        @error="imagePreviewError = true"
        @load="imagePreviewError = false"
      />
      <span v-if="imagePreviewError" class="text-red-500 ml-2">URL รูปภาพไม่ถูกต้อง</span>
    </div>
    <button
      @click="createNote"
      class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white p-2 rounded-md w-full mb-6 font-semibold shadow-md transition"
    >
      ➕ Add Note
    </button>

    <!-- Search -->
    <input
      v-model="searchMyQuery"
      placeholder="🔍 Search your notes..."
      class="bg-gray-800 text-white border border-gray-700 p-3 rounded-md w-full mb-4 focus:outline-none focus:ring focus:ring-blue-500 shadow-sm"
      @input="debouncedSearchMy"
    />

    <!-- Notes in Grid -->
    <div v-if="myNotes.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <div
        v-for="note in myNotes"
        :key="note.id"
        class="bg-gray-900 border border-gray-700 p-4 rounded-md relative group transition transform hover:-translate-y-1 hover:shadow-lg min-h-[300px] flex flex-col justify-between"
      >
        <div>
          <div class="flex justify-between items-center mb-2">
            <h2 v-if="editNoteId !== note.id" class="text-xl font-semibold">{{ note.title }}</h2>
            <div class="flex space-x-2 items-center">
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
            <p class="text-gray-300 mt-2 whitespace-pre-wrap text-sm">{{ note.content }}</p>
            <div v-if="note.image_url" class="mt-2">
              <img
                :src="note.image_url"
                alt="Note Image"
                class="w-full h-32 object-cover rounded"
              />
            </div>
          </div>
        </div>

        <div
          class="absolute bottom-2 right-2 bg-gray-800 text-xs text-gray-400 px-2 py-1 rounded select-none z-10 italic"
          style="white-space: nowrap;"
        >
          ✍️ <span class="font-semibold">{{ note.username || 'Unknown' }}</span>
        </div>
      </div>
    </div>

    <div v-else class="text-gray-500 mt-8 text-center text-lg">
      🗒️ No notes to display
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const title = ref('')
const content = ref('')
const imageUrl = ref('')
const imagePreviewError = ref(false)

const myNotes = ref([])
const searchMyQuery = ref('')
const token = localStorage.getItem('token')

const editNoteId = ref(null)
const editTitle = ref('')
const editContent = ref('')
const editImageUrl = ref('')

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

let timeoutMy
const debouncedSearchMy = () => {
  clearTimeout(timeoutMy)
  timeoutMy = setTimeout(() => {
    searchMyNotes()
  }, 300)
}

onMounted(() => {
  fetchMyNotes()
})
</script>


<style>
.btn-black {
  background-color: #111827;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid transparent;
}
</style>

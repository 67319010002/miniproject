<template>
  <div class="min-h-screen bg-black text-white p-6 max-w-6xl mx-auto grid grid-cols-10 gap-8">
    <div class="col-span-7">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold">Share Notes with me</h1>
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

      <div v-if="allNotes.length > 0" class="grid grid-cols-4 gap-6">
  
  <div
    v-for="note in allNotes"
    :key="note.id"
    @click="openNoteModal(note)"
    :class="[
      'border rounded-md relative cursor-pointer note-hover-effect flex flex-col p-4',
      note.id === selectedNote?.id
        ? 'bg-white text-black border-gray-400'
        : isFavorite(note.id)
        ? 'bg-gray-700 text-white border-gray-600'
        : 'bg-gray-900 text-white border-gray-700'
    ]"
    style="aspect-ratio: 4 / 3; display: flex; flex-direction: column;"
  >
    <h2 class="text-xl font-semibold truncate">{{ note.title }}</h2>

    <div
      class="text-sm mt-1 select-none"
      :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-400'"
    >
      ❤️ {{ note.favorite_count || 0 }} Favorites
    </div>
    <div
      class="text-sm mt-1 select-none"
      :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-400'"
    >
      💬 {{ note.comment_count || 0 }} Comments
    </div>

    <p
      class="mt-2 flex-grow overflow-hidden"
      :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-300'"
      style="display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden;"
    >
      {{ note.content }}
    </p>

    <div v-if="note.image_url" class="mt-4 flex-shrink-0">
      <img
        :src="note.image_url"
        alt="Note Image"
        class="w-full h-28 object-cover rounded"
      />
    </div>

    <div
      class="flex items-center gap-2 mt-auto select-none pt-2 border-t border-gray-700"
      :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-300'"
      style="white-space: nowrap;"
    >
      <img
        v-if="note.user_profile_pic"
        :src="getFullProfilePicURL(note.user_profile_pic)"
        alt="User Profile"
        class="w-6 h-6 rounded-full object-cover"
      />
      <div
        v-else
        class="w-6 h-6 rounded-full bg-gray-700 flex items-center justify-center text-white font-bold text-xs select-none"
      >
        {{ note.username ? note.username.charAt(0).toUpperCase() : "?" }}
      </div>
      <span :class="note.id === selectedNote?.id ? 'font-semibold text-black' : 'font-semibold'">
        {{ note.username || 'Unknown' }}
      </span>
    </div>

    <button
      @click.stop="toggleFavorite(note.id)"
      class="favorite-btn absolute bottom-3 right-3 text-xl"
      :title="isFavorite(note.id) ? 'Remove from favorites' : 'Add to favorites'"
    >
      <span
        :class="{
          'text-red-500': isFavorite(note.id),
          'text-gray-500': !isFavorite(note.id),
        }"
      >❤️</span>
    </button>
  </div>
</div>

      <div v-else class="text-gray-500 mt-8">No notes to display</div>
    </div>

    <div class="col-span-3 border-l border-gray-700 pl-6">
      <h1 class="text-2xl font-bold mb-4">❤️ Favorites</h1>
      <div v-if="favoriteNotesList.length > 0" class="space-y-4">
        <div
          v-for="note in favoriteNotesList"
          :key="note.id"
          @click="openNoteModal(note)"
          :class="[
            'border p-3 rounded-md cursor-pointer note-hover-effect flex items-center gap-3 relative',
            note.id === selectedNote?.id
              ? 'bg-white text-black border-gray-400'
              : 'bg-gray-800 text-gray-300 border-gray-600',
          ]"
        >
          <div
            class="w-16 h-16 flex-shrink-0 rounded overflow-hidden"
            :class="note.id === selectedNote?.id ? 'bg-white' : 'bg-gray-700'"
          >
            <img
              v-if="note.image_url"
              :src="note.image_url"
              alt="Note Image"
              class="w-full h-full object-cover"
            />
            <div
              v-else
              class="w-full h-full flex items-center justify-center text-gray-500 text-sm"
            >
              No Image
            </div>
          </div>

          <div class="flex-1 min-w-0">
            <h3 :class="['font-semibold text-lg mb-1 truncate', note.id === selectedNote?.id ? 'text-black' : 'text-white']">
              {{ note.title }}
            </h3>

            <div
              class="text-xs text-gray-400 mb-1 select-none"
              :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-400'"
            >
              ❤️ {{ note.favorite_count || 0 }} Favorites
            </div>
            
            <div
              class="text-xs text-gray-400 mb-1 select-none"
              :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-400'"
            >
              💬 {{ note.comment_count || 0 }} Comments
            </div>

            <p :class="['truncate text-sm', note.id === selectedNote?.id ? 'text-black' : 'text-gray-400']">
              {{ note.content }}
            </p>
          </div>

          <button
            @click.stop="toggleFavorite(note.id)"
            class="favorite-btn absolute bottom-3 right-3 text-xl"
            :title="isFavorite(note.id) ? 'Remove from favorites' : 'Add to favorites'"
          >
            <span
              :class="{
                'text-red-500': isFavorite(note.id),
                'text-gray-500': !isFavorite(note.id),
              }"
            >❤️</span>
          </button>
        </div>
      </div>
      
    </div>

    
    <div
  v-if="selectedNote"
  class="fixed inset-0 flex items-center justify-center z-50"
  @click.self="closeNoteModal"
  style="background-color: rgba(0, 0, 0, 0.4); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);"
>
  <div
    class="bg-white p-6 rounded-md shadow-lg relative flex"
    style="width: 750px; height: 500px; overflow: hidden;"
  >
    <button
      @click="closeNoteModal"
      class="absolute top-2 right-2 text-gray-700 hover:text-black text-xl font-bold"
      aria-label="Close modal"
    >
      &times;
    </button>

    <!-- ซ้าย: เนื้อหาโน้ต -->
    <div
      class="note-content"
      style="flex: 1 1 60%; overflow-y: auto; padding-right: 12px;"
    >
      <!-- ชื่อผู้เขียน + หัวใจ -->
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
          <img
            v-if="selectedNote.user_profile_pic"
            :src="getFullProfilePicURL(selectedNote.user_profile_pic)"
            alt="User Profile"
            class="w-8 h-8 rounded-full object-cover"
          />
          <div
            v-else
            class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-white font-bold text-sm select-none"
          >
            {{ selectedNote.username ? selectedNote.username.charAt(0).toUpperCase() : "?" }}
          </div>
          <span class="font-semibold text-black">
            {{ selectedNote.username || 'Unknown' }}
          </span>
        </div>

      </div>

      <!-- ชื่อโน้ต -->
      <h2 class="text-2xl font-bold mb-2 text-black">{{ selectedNote.title }}</h2>

      <!-- เนื้อหาโน้ต -->
      <p
        class="whitespace-pre-wrap text-gray-900 mb-4"
        style="max-height: 100px; overflow-y: auto;"
      >
        {{ selectedNote.content }}
      </p>

      <div v-if="selectedNote.image_url" class="mt-2">
        <img
          :src="selectedNote.image_url"
          alt="Note Image"
          class="w-full max-h-60 object-contain rounded"
        />
      </div>
      <button
      @click.stop="toggleFavorite(selectedNote.id)"
      class="favorite-btn text-2xl"
      :title="isFavorite(selectedNote.id) ? 'Remove from favorites' : 'Add to favorites'"
      style="position: absolute; left: 12px; bottom: 12px; cursor: pointer; user-select: none;"
    >
      <span
        :class="{
          'text-red-500': isFavorite(selectedNote.id),
          'text-gray-400': !isFavorite(selectedNote.id),
        }"
      >❤️</span>
    </button>


    </div>

    <div
    class="note-comments"
    style="flex: 1 1 40%; border-left: 1px solid #ddd; padding-left: 12px; display: flex; flex-direction: column; height: 100%;"
>
    <h3 class="text-xl font-semibold mb-4">Comments ({{ noteComments.length }})</h3>
    <div
        class="comments-list flex-grow overflow-y-auto pr-2"
        style="min-height: 0;"
    >
        <div v-if="noteComments.length > 0">
            <div
                v-for="comment in noteComments"
                :key="comment.id"
                class="p-3 bg-gray-100 rounded-md mb-2"
            >
                <div class="flex justify-between items-center text-sm font-semibold text-gray-800">
                    {{ comment.username }}
                    <button
                        v-if="comment.username === username"
                        @click="deleteComment(comment.id, selectedNote.id)"
                        class="text-red-500 hover:text-red-700 text-xs"
                        title="Delete comment"
                    >
                        &times; Delete
                    </button>
                </div>

                <p class="mt-1 text-gray-700">{{ comment.content }}</p>

                <div class="text-right">
                    <span class="text-xs text-gray-500">{{ comment.created_at }}</span>
                </div>
            </div>
        </div>
        <div v-else class="text-gray-500 text-center">No comments yet.</div>
    </div>

    <form @submit.prevent="submitComment" class="mt-4">
        <textarea
            v-model="newCommentContent"
            placeholder="Write a comment..."
            class="w-full p-2 text-sm text-gray-900 bg-gray-100 rounded-md focus:outline-none focus:ring focus:ring-blue-500"
            rows="3"
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
import axios from "axios";
import { ref, onMounted, computed, watch } from "vue";
import { debounce } from "lodash";

const allNotes = ref([]);
const searchAllQuery = ref("");
const token = localStorage.getItem("token");
const username = ref(localStorage.getItem("username") || "guest");

// ดึงค่าจาก .env
const backendBaseURL = import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:5000";

// raw path รูปโปรไฟล์จาก localStorage
const profilePicRaw = ref(localStorage.getItem("profilePic") || "");

// แปลง path เป็น URL เต็ม
const profilePic = computed(() => {
  if (!profilePicRaw.value) return "";
  if (profilePicRaw.value.startsWith("http://") || profilePicRaw.value.startsWith("https://")) {
    return profilePicRaw.value;
  }
  return backendBaseURL + profilePicRaw.value;
});

const usernameInitial = computed(() => {
  return username.value ? username.value.charAt(0).toUpperCase() : "";
});

const selectedNote = ref(null);
const newCommentContent = ref('');
const noteComments = ref([]);

// ดึงคอมเมนต์
const fetchComments = async (noteId) => {
  try {
    const res = await axios.get(`${backendBaseURL}/api/comments/${noteId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    noteComments.value = res.data;
  } catch (e) {
    console.error('Failed to fetch comments:', e);
  }
};

const submitComment = async () => {
  if (!newCommentContent.value.trim()) return;
  try {
    const res = await axios.post(
      `${backendBaseURL}/api/comments/${selectedNote.value.id}`,
      { content: newCommentContent.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    // โค้ดสำคัญ: เพิ่มคอมเมนต์ใหม่ลงในอาร์เรย์ทันที
    noteComments.value.unshift(res.data);
    newCommentContent.value = '';

    // อัปเดตจำนวนคอมเมนต์บนหน้าจอ
    const noteIndex = allNotes.value.findIndex(note => note.id === selectedNote.value.id);
    if (noteIndex !== -1) {
      allNotes.value[noteIndex].comment_count = noteComments.value.length;
    }
    if (selectedNote.value) {
      selectedNote.value.comment_count = noteComments.value.length;
    }
  } catch (e) {
    console.error('Failed to post comment:', e);
  }
};

const openNoteModal = (note) => {
  selectedNote.value = note;
  if (note && note.id) {
    fetchComments(note.id);
  }
};
const closeNoteModal = () => {
  selectedNote.value = null;
  noteComments.value = [];
  newCommentContent.value = '';
};

// ลบคอมเมนต์
const deleteComment = async (commentId, noteId) => {
  if (!confirm("Are you sure you want to delete this comment?")) return;
  try {
    const res = await axios.delete(`${backendBaseURL}/api/comments/${commentId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (res.status === 200) {
      noteComments.value = noteComments.value.filter(comment => comment.id !== commentId);
      const noteIndex = allNotes.value.findIndex(note => note.id === noteId);
      if (noteIndex !== -1) {
        allNotes.value[noteIndex].comment_count = noteComments.value.length;
      }
    }
  } catch (e) {
    console.error('Failed to delete comment:', e);
  }
};

const getFullProfilePicURL = (path) => {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return backendBaseURL + path;
};

const favoriteNotes = ref(new Set());

// โหลด favorite
const loadFavoritesFromBackend = async () => {
  try {
    const res = await axios.get(`${backendBaseURL}/api/favorites`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const favIds = res.data.map((note) => note.id);
    favoriteNotes.value = new Set(favIds);
  } catch (e) {
    console.error("Failed to load favorites from backend:", e);
    favoriteNotes.value = new Set();
  }
};

// toggle favorite
const toggleFavorite = async (noteId) => {
  try {
    await axios.post(
      `${backendBaseURL}/api/favorites/${noteId}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (favoriteNotes.value.has(noteId)) {
      favoriteNotes.value.delete(noteId);
    } else {
      favoriteNotes.value.add(noteId);
    }
  } catch (e) {
    console.error("Failed to toggle favorite:", e);
  }
};

const isFavorite = (noteId) => favoriteNotes.value.has(noteId);

const favoriteNotesList = computed(() => {
  return allNotes.value.filter((note) => favoriteNotes.value.has(note.id));
});

const fetchAllNotes = async () => {
  try {
    const res = await axios.get(`${backendBaseURL}/api/notes/all`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    allNotes.value = res.data;
  } catch (e) {
    console.error("Failed to fetch all notes:", e);
  }
};

const searchAllNotes = async () => {
  const q = searchAllQuery.value.trim();
  if (!q) return fetchAllNotes();
  try {
    const res = await axios.get(
      `${backendBaseURL}/api/notes/all/search?q=${encodeURIComponent(q)}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    allNotes.value = res.data;
  } catch (e) {
    console.error("Failed to search all notes:", e);
  }
};

const debouncedSearchAll = debounce(() => {
  searchAllNotes();
}, 300);

watch(username, () => {
  loadFavoritesFromBackend();
  fetchAllNotes();
});

onMounted(() => {
  loadFavoritesFromBackend();
  fetchAllNotes();
});
</script>


<style>
html,
body {
  background-color: #000;
}

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

.favorite-btn span {
  display: inline-block;
  transition: transform 0.2s ease;
}

.favorite-btn:hover span {
  transform: scale(1.3) translateY(-4px);
}

.favorite-btn.absolute {
  position: absolute;
}
</style>
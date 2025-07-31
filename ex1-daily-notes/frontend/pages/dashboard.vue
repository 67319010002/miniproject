<template>
  <div class="min-h-screen bg-black text-white p-6 max-w-6xl mx-auto grid grid-cols-10 gap-8">
    <!-- All Notes (ซ้าย 7 คอลัมน์) -->
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
            'border p-4 rounded-md relative cursor-pointer note-hover-effect flex flex-col',
            note.id === selectedNote?.id
              ? 'bg-white text-black border-gray-400'
              : isFavorite(note.id)
              ? 'bg-gray-700 text-white border-gray-600'
              : 'bg-gray-900 text-white border-gray-700'
          ]"
          style="aspect-ratio: 4 / 3;"
        >
          <h2 class="text-xl font-semibold truncate">{{ note.title }}</h2>

          <!-- แสดงจำนวนแฟโวริท -->
          <div
            class="text-sm mt-1 select-none"
            :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-400'"
          >
            ❤️ {{ note.favorite_count || 0 }} Favorites
          </div>

          <p
            class="mt-2 flex-grow overflow-hidden"
            :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-300'"
            style="display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden;"
          >
            {{ note.content }}
          </p>

          <div v-if="note.image_url" class="mt-4 mb-0 flex-shrink-0">
            <img
              :src="note.image_url"
              alt="Note Image"
              class="w-full h-auto object-contain rounded"
              style="max-height: 120px;"
            />
          </div>

          <div
            class="text-xs mt-2 select-none"
            :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-300'"
            style="white-space: nowrap;"
          >
            Written by:
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

    <!-- Favorite Notes (ขวา 3 คอลัมน์) -->
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

            <!-- แสดงจำนวนแฟโวริท -->
            <div
              class="text-xs text-gray-400 mb-1 select-none"
              :class="note.id === selectedNote?.id ? 'text-black' : 'text-gray-400'"
            >
              ❤️ {{ note.favorite_count || 0 }} Favorites
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
      <div v-else class="text-gray-500">No favorite notes yet.</div>
    </div>

    <!-- Modal Popup for Selected Note -->
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
          Written by:
          <span class="font-semibold">{{ selectedNote.username || 'Unknown' }}</span>
        </div>

        <button
          @click.stop="toggleFavorite(selectedNote.id)"
          class="favorite-btn absolute bottom-4 right-4 text-3xl"
          :title="isFavorite(selectedNote.id) ? 'Remove from favorites' : 'Add to favorites'"
        >
          <span
            :class="{
              'text-red-500': isFavorite(selectedNote.id),
              'text-gray-500': !isFavorite(selectedNote.id),
            }"
          >❤️</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, computed, watch } from "vue";

const allNotes = ref([]);
const searchAllQuery = ref("");
const token = localStorage.getItem("token");

// reactive username
const username = ref(localStorage.getItem("username") || "guest");

const selectedNote = ref(null);
const openNoteModal = (note) => {
  selectedNote.value = note;
};
const closeNoteModal = () => {
  selectedNote.value = null;
};

// ใช้ Set เก็บ favorite note ids
const favoriteNotes = ref(new Set());

// โหลด favorite notes จาก backend (API)
const loadFavoritesFromBackend = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/favorites", {
      headers: { Authorization: `Bearer ${token}` },
    });
    // ดึง note ids จาก response
    const favIds = res.data.map((note) => note.id);
    favoriteNotes.value = new Set(favIds);
  } catch (e) {
    console.error("Failed to load favorites from backend:", e);
    favoriteNotes.value = new Set();
  }
};

// toggle favorite และ sync กับ backend
const toggleFavorite = async (noteId) => {
  try {
    // เรียก API POST toggle favorite ที่ backend
    await axios.post(
      `http://localhost:5000/api/favorites/${noteId}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );

    // อัปเดต favoriteNotes local หลัง API สำเร็จ
    if (favoriteNotes.value.has(noteId)) {
      favoriteNotes.value.delete(noteId);
    } else {
      favoriteNotes.value.add(noteId);
    }
  } catch (e) {
    console.error("Failed to toggle favorite:", e);
  }
};

const isFavorite = (noteId) => {
  return favoriteNotes.value.has(noteId);
};

const favoriteNotesList = computed(() => {
  return allNotes.value.filter((note) => favoriteNotes.value.has(note.id));
});

const fetchAllNotes = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/notes/all", {
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
      `http://localhost:5000/api/notes/all/search?q=${encodeURIComponent(q)}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    allNotes.value = res.data;
  } catch (e) {
    console.error("Failed to search all notes:", e);
  }
};

let timeoutAll;
const debouncedSearchAll = () => {
  clearTimeout(timeoutAll);
  timeoutAll = setTimeout(() => {
    searchAllNotes();
  }, 300);
};

// เมื่อ username เปลี่ยน หรือโหลดครั้งแรก ให้โหลด favorites และ notes
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

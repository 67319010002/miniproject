<template>
  <div class="bg-white p-4 shadow rounded mb-3">
    <h2 class="font-bold">{{ note.title }}</h2>

    <!-- แสดงรูปภาพถ้ามี -->
    <div v-if="note.image_url" class="my-2">
      <img 
        :src="note.image_url" 
        alt="Note Image" 
        class="w-full max-h-60 object-contain rounded"
      />
    </div>

    <p class="text-sm text-gray-600">{{ note.content }}</p>
    <p class="text-xs text-right">{{ note.created_at }}</p>
    <p class="text-xs text-right italic text-gray-500 mt-1">
      Written by: <span class="font-semibold text-gray-700">{{ user }}</span>
    </p>
    <button
      @click="$emit('delete', note.id)"
      class="text-red-500 text-sm mt-2 hover:text-red-700 transition"
    >
      Delete
    </button>
  </div>
</template>

<script setup>
defineProps({
  note: Object,
  user: String,
})
defineEmits(['delete'])
</script>

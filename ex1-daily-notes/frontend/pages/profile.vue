<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm text-center">
      <h1 class="text-2xl font-bold text-white mb-6">My Profile</h1>

      <!-- รูปโปรไฟล์ -->
      <img
        v-if="fullImageUrl"
        :src="fullImageUrl"
        alt="Profile"
        class="w-32 h-32 rounded-full mx-auto mb-4 object-cover border-4 border-white"
      />
      <div v-else class="w-32 h-32 rounded-full mx-auto mb-4 bg-gray-600 flex items-center justify-center text-white text-sm">
        No Image
      </div>

      <div class="text-white mb-4">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email || '-' }}</p>
      </div>

      <button
        @click="handleLogout"
        class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200"
      >
        Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref({
  username: '',
  email: '',
  profile_image_url: ''
})

// กำหนด base URL ของ backend ให้ตรงกับที่เซิร์ฟเวอร์รัน (เช่น localhost:5000)
const baseURL = 'http://localhost:5000'

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (!storedUser) {
    router.push('/login')
    return
  }

  try {
    const parsedUser = JSON.parse(storedUser)

    user.value = parsedUser
  } catch (e) {
    console.error('Error parsing user from localStorage', e)
    router.push('/login')
  }
})

// computed เพื่อคืน full URL ของรูปภาพ
const fullImageUrl = computed(() => {
  if (!user.value.profile_image_url) return null
  // ถ้า URL เริ่มด้วย http ให้ใช้ตรง ๆ
  if (user.value.profile_image_url.startsWith('http')) return user.value.profile_image_url
  // ถ้าเป็น path เช่น /static/uploads/xxx.jpg ให้เติม baseURL หน้า path
  return baseURL + user.value.profile_image_url
})

const handleLogout = () => {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

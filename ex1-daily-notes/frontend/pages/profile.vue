<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center mb-6">My Profile</h1>

      <div class="text-white mb-4">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref({ username: '', email: '' })

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (!storedUser) {
    router.push('/login') // ถ้าไม่มี user ให้ไปหน้า login
    return
  }
  user.value = JSON.parse(storedUser)
})

const handleLogout = () => {
  localStorage.removeItem('user')
  localStorage.removeItem('token') // ถ้ามี token ด้วย
  router.push('/login')
}
</script>

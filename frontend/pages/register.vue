<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center mb-6">Register</h1>

      <input
        v-model="username"
        placeholder="Username"
        class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      />

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      />

      <!-- ✅ ฟิลด์เลือกรูป -->
      <input
        type="file"
        @change="onFileChange"
        accept="image/*"
        class="mb-4 p-3 w-full text-sm text-gray-400 file:bg-gray-700 file:border-none file:p-2 file:text-white rounded-lg bg-gray-700"
      />

      <button
        @click="handleRegister"
        class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      >
        Register
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">
        {{ errorMsg }}
      </p>
      <p v-if="successMsg" class="text-green-400 text-sm mt-4 text-center">
        {{ successMsg }}
      </p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Already have an account?
        <router-link to="/login" class="underline hover:text-white">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import.meta.env.VITE_BACKEND_BASE_URL
const username = ref('')
const email = ref('')
const password = ref('')
const profileImage = ref(null)

const errorMsg = ref('')
const successMsg = ref('')
const router = useRouter()
const backendBaseURL = import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:5000";

const onFileChange = (e) => {
  profileImage.value = e.target.files[0]
}

const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (!username.value || !email.value || !password.value) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }

  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('email', email.value)
    formData.append('password', password.value)

    if (profileImage.value) {
      formData.append('profile_image', profileImage.value)
    }

    const res = await axios.post(`${backendBaseURL}/api/register`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // เก็บข้อมูล user ที่ได้จาก response (เช่น profile_image_url) ลง localStorage
    if (res.data.user) {
      localStorage.setItem('user', JSON.stringify(res.data.user))
    } else {
      // fallback กรณีไม่มี user ใน response
      localStorage.setItem('user', JSON.stringify({
        username: username.value,
        email: email.value,
        profile_image_url: ''
      }))
    }

    successMsg.value = 'Registration successful. Redirecting to login...'
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err) {
    errorMsg.value =
      err.response?.data?.msg || 'Registration failed. Please try again.'
  }
}
</script>

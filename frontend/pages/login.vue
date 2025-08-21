<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center mb-6">Login</h1>

      <input
        v-model="username"
        placeholder="Username"
        class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-4 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      />

      <button
        @click="handleLogin"
        class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      >
        Login
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">
        {{ errorMsg }}
      </p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Don’t have an account?
        <router-link to="/register" class="underline hover:text-white">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import.meta.env.VITE_BACKEND_BASE_URL

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()
const backendBaseURL = import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:5222";

function updateUsername(newUsername) {
  localStorage.setItem('username', newUsername)
  username.value = newUsername
}

const handleLogin = async () => {
  errorMsg.value = ''

  if (!username.value || !password.value) {
    errorMsg.value = 'Please enter username and password.'
    return
  }

  try {
    const res = await axios.post(`${backendBaseURL}/api/login`, {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', res.data.access_token)

    if (res.data.user) {
      localStorage.setItem(
        'user',
        JSON.stringify({
          username: res.data.user.username,
          email: res.data.user.email,
          profile_image_url: res.data.user.profile_image_url || ''
        })
      )
      updateUsername(res.data.user.username)
    }

    router.push('/dashboard')
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Login failed. Please try again.'
    password.value = ''
  }
}
</script>

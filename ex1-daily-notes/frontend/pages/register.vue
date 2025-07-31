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
        class="mb-4 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
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
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const router = useRouter()

const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (!username.value || !email.value || !password.value) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }

  try {
    await axios.post('http://localhost:5000/api/register', {
      username: username.value,
      email: email.value,
      password: password.value
    })

    // บันทึกข้อมูล user ลง localStorage
    localStorage.setItem('user', JSON.stringify({
      username: username.value,
      email: email.value
    }))

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

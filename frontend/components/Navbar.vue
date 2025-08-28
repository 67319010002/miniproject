<template>
  <nav class="bg-black text-white px-6 py-4 flex items-center shadow-md relative">
    <!-- ชื่อแอป -->
    <NuxtLink
      to="/dashboard"
      class="font-bold text-2xl flex-shrink-0 transition-all duration-300 transform hover:scale-105 hover:text-gray-300 hover:shadow-lg hover:brightness-110"
    >
      ShareNote
    </NuxtLink>

    <!-- ปุ่มทางขวา -->
    <div class="ml-auto flex items-center gap-3">

      <!-- ยังไม่ล็อกอิน -->
      <template v-if="!isLoggedIn">
        <NuxtLink
          to="/register"
          class="px-4 py-2 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 text-white font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-xl hover:from-blue-600 hover:to-blue-700 hover:brightness-110"
        >
          ✨ Register
        </NuxtLink>
      </template>

      <!-- ล็อกอินแล้ว -->
      <template v-else>
        <!-- My Notes -->
        <NuxtLink
          to="/mynotes"
          class="px-4 py-2 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-xl hover:from-blue-600 hover:to-cyan-600 hover:brightness-110 flex items-center gap-1"
          @click="closeDropdown"
        >
          My Notes
        </NuxtLink>

        <!-- Favorites -->
        <NuxtLink
          to="/favoritenotes"
          class="px-4 py-2 rounded-full bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold flex items-center gap-1 transition-all duration-300 transform hover:scale-105 hover:shadow-xl hover:from-cyan-600 hover:to-blue-600 hover:brightness-110"
          @click="closeDropdown"
        >
          ❤️ 
        </NuxtLink>

        <!-- Profile รูปกลม -->
        <NuxtLink
          to="/profile"
          class="w-10 h-10 rounded-full overflow-hidden border-2 border-gray-700 flex-shrink-0 transition-all duration-300 transform hover:scale-110 hover:shadow-xl hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          @click="closeDropdown"
        >
          <img
            v-if="userProfilePic"
            :src="fullImageUrl"
            alt="Profile"
            class="w-full h-full object-cover transition-transform duration-300 transform hover:scale-125 hover:rotate-3 hover:shadow-xl hover:brightness-110"
          />
          <div
            v-else
            class="w-full h-full bg-gray-700 flex items-center justify-center text-white font-bold text-sm transition-all duration-300 transform hover:scale-110 hover:shadow-xl hover:brightness-110"
          >
            {{ usernameInitial }}
          </div>
        </NuxtLink>

        <!-- Settings dropdown -->
        <div class="relative">
          <button
            ref="btnRef"
            @click="toggleDropdown"
            class="p-2 rounded hover:bg-gray-800 transition-all duration-300 transform hover:scale-110 hover:shadow-xl hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Settings"
          >
            ⚙️
          </button>

          <transition
            name="dropdown"
            enter-active-class="transition ease-out duration-300"
            enter-from-class="opacity-0 translate-y-2 scale-95"
            enter-to-class="opacity-100 translate-y-0 scale-100"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="opacity-100 translate-y-0 scale-100"
            leave-to-class="opacity-0 translate-y-2 scale-95"
          >
            <div
              v-if="dropdownOpen"
              ref="menuRef"
              class="absolute right-0 mt-2 w-40 bg-gray-900 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
            >
              <button
                @click="handleLogout"
                class="w-full text-left px-4 py-2 text-red-400 transition-all duration-300 transform hover:bg-gray-700 hover:scale-105 hover:-translate-y-1 hover:shadow-xl hover:brightness-110"
              >
                Logout
              </button>
            </div>
          </transition>
        </div>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const dropdownOpen = ref(false)
const btnRef = ref(null)
const menuRef = ref(null)
const router = useRouter()

const isLoggedIn = ref(false)
const username = ref('guest')
const userProfilePic = ref('')

const usernameInitial = computed(() => username.value.charAt(0).toUpperCase())

const backendBaseURL = import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:5222"
const fullImageUrl = computed(() => {
  if (!userProfilePic.value) return null
  if (userProfilePic.value.startsWith('http')) return userProfilePic.value
  if (userProfilePic.value.startsWith('/static')) return `${backendBaseURL}${userProfilePic.value}`
  return `${backendBaseURL}/static/uploads/${userProfilePic.value}`
})

const loadAuthState = () => {
  if (!process.client) return
  const token = localStorage.getItem('token')
  isLoggedIn.value = !!token

  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      const parsedUser = JSON.parse(storedUser)
      username.value = parsedUser.username || 'guest'
      userProfilePic.value = parsedUser.profile_image_url || ''
    } catch {
      username.value = 'guest'
      userProfilePic.value = ''
    }
  } else {
    username.value = 'guest'
    userProfilePic.value = ''
  }
}

onMounted(() => {
  loadAuthState()
  window.addEventListener('click', handleClickOutside)
  window.addEventListener('auth-changed', loadAuthState)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
  window.removeEventListener('auth-changed', loadAuthState)
})

const toggleDropdown = () => dropdownOpen.value = !dropdownOpen.value
const closeDropdown = () => dropdownOpen.value = false

const handleLogout = () => {
  if (process.client) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
  closeDropdown()
  loadAuthState()
  router.push('/login')
}

const handleClickOutside = (event) => {
  const btn = btnRef.value
  const menu = menuRef.value
  if (dropdownOpen.value && menu && btn && !menu.contains(event.target) && !btn.contains(event.target)) {
    closeDropdown()
  }
}
</script>

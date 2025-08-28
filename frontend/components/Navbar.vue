<template>
  <nav class="bg-black text-white px-6 py-4 flex items-center shadow-md relative">
    <!-- ชื่อแอป -->
    <NuxtLink
      to="/dashboard"
      class="font-bold text-2xl hover:text-gray-300 transition flex-shrink-0"
    >
      ShareNote
    </NuxtLink>

    <!-- ปุ่มต่างๆ ทางขวา -->
    <div class="ml-auto flex items-center gap-3">
      
      <!-- ถ้ายังไม่ล็อกอิน -->
      <template v-if="!isLoggedIn">
        <NuxtLink
          to="/register"
          class="px-3 py-2 rounded bg-indigo-600 hover:bg-indigo-700 transition text-white font-semibold"
        >
          ✨ Register
        </NuxtLink>
      </template>

      <!-- ถ้าล็อกอินแล้ว -->
      <template v-else>
        <NuxtLink
          to="/mynotes"
          class="px-3 py-2 rounded bg-green-600 hover:bg-green-700 transition text-white font-semibold"
          @click="closeDropdown"
        >
          📝 My Notes
        </NuxtLink>

        <NuxtLink
          to="/favoritenotes"
          class="px-3 py-2 rounded bg-pink-600 hover:bg-pink-700 transition text-white font-semibold flex items-center gap-1"
          @click="closeDropdown"
        >
          ❤️ Favorites
        </NuxtLink>

        <NuxtLink
          to="/profile"
          class="px-3 py-2 rounded hover:bg-gray-800 transition focus:outline-none focus:ring-2 focus:ring-indigo-500"
          @click="closeDropdown"
        >
          👤 Profile
        </NuxtLink>

        <!-- ปุ่มฟันเฟือง + dropdown -->
        <div class="relative">
          <button
            ref="btnRef"
            @click="toggleDropdown"
            class="p-2 rounded hover:bg-gray-800 transition focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Settings"
          >
            ⚙️
          </button>

          <div
            v-if="dropdownOpen"
            ref="menuRef"
            class="absolute right-0 mt-2 w-40 bg-gray-900 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
          >
            <button
              @click="handleLogout"
              class="w-full text-left px-4 py-2 text-red-400 hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
            >
              Logout
            </button>
          </div>
        </div>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const dropdownOpen = ref(false)
const btnRef = ref(null)
const menuRef = ref(null)
const router = useRouter()

// reactive state เก็บสถานะการล็อกอิน
const isLoggedIn = ref(false)

// โหลดสถานะตอนเปิดหน้า
onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('token')
  window.addEventListener('click', handleClickOutside)

  // ✅ ฟัง event เวลา login/logout จากหน้าอื่น
  window.addEventListener('auth-changed', updateAuthState)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
  window.removeEventListener('auth-changed', updateAuthState)
})

const updateAuthState = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('user')
  closeDropdown()
  // อัปเดต navbar ทันที
  updateAuthState()
  router.push('/login')
}

const handleClickOutside = (event) => {
  const btn = btnRef.value
  const menu = menuRef.value
  if (
    dropdownOpen.value &&
    menu &&
    btn &&
    !menu.contains(event.target) &&
    !btn.contains(event.target)
  ) {
    closeDropdown()
  }
}
</script>

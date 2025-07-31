<template>
  <nav class="bg-black text-white px-6 py-4 flex items-center shadow-md relative">
    <!-- ชื่อแอป -->
    <NuxtLink to="/dashboard" class="font-bold text-2xl hover:text-gray-300 transition flex-shrink-0">
      ShareNote
    </NuxtLink>

    <!-- ปุ่มต่างๆ ทางขวา -->
    <div class="ml-auto flex items-center gap-3">
      
      <!-- ปุ่มไปหน้า My Notes -->
      <NuxtLink
        to="/mynotes"
        class="px-3 py-2 rounded bg-green-600 hover:bg-green-700 transition text-white font-semibold"
        @click="closeDropdown"
      >
        📝 My Notes
      </NuxtLink>

      <!-- ปุ่มไปหน้า Favorite Notes -->
      <NuxtLink
        to="/favoritenotes"
        class="px-3 py-2 rounded bg-pink-600 hover:bg-pink-700 transition text-white font-semibold flex items-center gap-1"
        @click="closeDropdown"
      >
        ❤️ Favorites
      </NuxtLink>

      <!-- ปุ่มโปรไฟล์ -->
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
          <NuxtLink
            to="/login"
            class="block px-4 py-2 text-white hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
            @click="closeDropdown"
          >
            Login
          </NuxtLink>
          <NuxtLink
            to="/register"
            class="block px-4 py-2 text-white hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
            @click="closeDropdown"
          >
            Register
          </NuxtLink>
          <NuxtLink
            to="/dashboard"
            class="block px-4 py-2 text-white hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
            @click="closeDropdown"
          >
            Dashboard
          </NuxtLink>
          <button
            @click="handleLogout"
            class="w-full text-left px-4 py-2 text-red-400 hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
          >
            Logout
          </button>
        </div>
      </div>
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

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogout = () => {
  // ลบข้อมูล token และ username ใน localStorage
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('user')

  closeDropdown()
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

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})
</script>

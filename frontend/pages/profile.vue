<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm text-center">
      <h1 class="text-2xl font-bold text-white mb-6">My Profile</h1>

      <div class="relative mx-auto w-32 h-32 mb-4">
        <img
          v-if="fullImageUrl"
          :src="fullImageUrl"
          alt="Profile"
          class="w-full h-full rounded-full object-cover border-4 border-white"
        />
        <div v-else class="w-full h-full rounded-full bg-gray-600 flex items-center justify-center text-white text-sm">
          No Image
        </div>
        <button
          @click="openImageUpload"
          :disabled="!isEditing"
          class="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2 disabled:opacity-50"
          title="Change Photo"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
        <input
          type="file"
          ref="fileInput"
          @change="handleImageUpload"
          accept="image/*"
          class="hidden"
        />
      </div>

      <div class="text-white mb-4 text-left">
        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Username</label>
          <input
            v-model="editForm.username"
            type="text"
            class="w-full bg-gray-700 rounded-lg px-3 py-2 text-white disabled:opacity-75"
            :disabled="!isEditing"
          />
        </div>
        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Email</label>
          <input
            v-model="editForm.email"
            type="email"
            class="w-full bg-gray-700 rounded-lg px-3 py-2 text-white disabled:opacity-75"
            :disabled="!isEditing"
          />
        </div>
      </div>

      <div class="flex space-x-2">
        <button
          v-if="!isEditing"
          @click="startEditing"
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 flex-1 rounded-lg transition duration-200"
        >
          Edit Profile
        </button>
        <template v-else>
          <button
            @click="saveChanges"
            :disabled="isLoading"
            class="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 flex-1 rounded-lg transition duration-200 disabled:opacity-75"
          >
            <span v-if="!isLoading">Save</span>
            <span v-else>Saving...</span>
          </button>
          <button
            @click="cancelEditing"
            :disabled="isLoading"
            class="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 flex-1 rounded-lg transition duration-200 disabled:opacity-75"
          >
            Cancel
          </button>
        </template>
      </div>

      <button
        @click="handleLogout"
        class="mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200"
      >
        Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const fileInput = ref(null)
const isEditing = ref(false)
const isLoading = ref(false)

const user = ref({
  id: '',
  username: '',
  email: '',
  profile_image_url: '',
  original_image_url: ''
})

const editForm = ref({
  username: '',
  email: '',
  profile_image: null
})

const baseURL = 'http://localhost:5000'

// ดึงข้อมูลโปรไฟล์
const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await axios.get(`${baseURL}/api/profile`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    // อัพเดทข้อมูลผู้ใช้
    user.value = {
      id: response.data.id, // แก้ไข: ดึง id จาก response
      username: response.data.username,
      email: response.data.email,
      profile_image_url: response.data.profile_image_url || '',
      original_image_url: response.data.profile_image_url || ''
    }
    
    // อัพเดทแบบฟอร์มแก้ไข
    editForm.value = {
      username: response.data.username,
      email: response.data.email,
      profile_image: null
    }
    
    // บันทึกข้อมูลใหม่ลง localStorage
    localStorage.setItem('user', JSON.stringify({
      id: user.value.id,
      username: user.value.username,
      email: user.value.email,
      profile_image_url: user.value.profile_image_url
    }))
  } catch (error) {
    console.error('Failed to fetch profile:', error)
    if (error.response?.status === 401) {
      handleLogout()
    } else {
      alert('Failed to load profile data')
    }
  }
}

// แสดง URL รูปภาพแบบเต็ม
const fullImageUrl = computed(() => {
  if (!user.value.profile_image_url) return null
  
  // ถ้าเป็น URL เต็ม (เช่น จาก social login)
  if (user.value.profile_image_url.startsWith('http')) {
    return user.value.profile_image_url
  }
  
  // ถ้าเป็น path ในระบบเรา
  if (user.value.profile_image_url.startsWith('/static')) {
    return `${baseURL}${user.value.profile_image_url}`
  }
  
  // กรณีอื่นๆ
  return `${baseURL}/static/uploads/${user.value.profile_image_url}`
})

// เปิด dialog เลือกไฟล์
const openImageUpload = () => {
  if (!isEditing.value) return
  fileInput.value.click()
}

// จัดการอัพโหลดรูปภาพ
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // ตรวจสอบประเภทไฟล์
  const validTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!validTypes.includes(file.type)) {
    alert('Please select a valid image file (JPEG, PNG, GIF)')
    return
  }

  // ตรวจสอบขนาดไฟล์ (ไม่เกิน 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('Image size should be less than 5MB')
    return
  }

  editForm.value.profile_image = file
  
  // แสดงตัวอย่างรูปภาพก่อนอัพโหลด
  const reader = new FileReader()
  reader.onload = (e) => {
    user.value.profile_image_url = e.target.result
  }
  reader.readAsDataURL(file)
}

// เริ่มโหมดแก้ไข
const startEditing = () => {
  isEditing.value = true
  user.value.original_image_url = user.value.profile_image_url
}

// ยกเลิกการแก้ไข
const cancelEditing = () => {
  isEditing.value = false
  editForm.value = {
    username: user.value.username,
    email: user.value.email,
    profile_image: null
  }
  user.value.profile_image_url = user.value.original_image_url
}

// บันทึกการเปลี่ยนแปลง
const saveChanges = async () => {
  isLoading.value = true
  
  try {
    const formData = new FormData()
    
    // เพิ่มข้อมูลที่เปลี่ยนแปลง
    if (editForm.value.username !== user.value.username) {
      formData.append('username', editForm.value.username)
    }
    
    if (editForm.value.email !== user.value.email) {
      formData.append('email', editForm.value.email)
    }
    
    if (editForm.value.profile_image) {
      formData.append('profile_image', editForm.value.profile_image)
    }

    const token = localStorage.getItem('token')
    const response = await axios.put(`${baseURL}/api/profile`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      timeout: 10000
    })

    // อัพเดทข้อมูลผู้ใช้หลังบันทึกสำเร็จ
    user.value = {
      ...user.value,
      username: response.data.user.username,
      email: response.data.user.email,
      profile_image_url: response.data.user.profile_image_url || user.value.profile_image_url
    }
    
    // ปิดโหมดแก้ไข
    isEditing.value = false
    
    // โหลดข้อมูลใหม่จากเซิร์ฟเวอร์
    await fetchUserProfile()
    
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Failed to update profile:', error)
    
    // คืนค่ารูปภาพเดิมเมื่อเกิดข้อผิดพลาด
    user.value.profile_image_url = user.value.original_image_url
    
    if (error.response) {
      if (error.response.status === 401) {
        handleLogout()
      } else {
        alert(error.response.data?.msg || 'Failed to update profile')
      }
    } else if (error.code === 'ECONNABORTED') {
      alert('Request timeout - please try again')
    } else {
      alert('Network error - please check your connection')
    }
  } finally {
    isLoading.value = false
  }
}

// ออกจากระบบ
const handleLogout = () => {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  router.push('/login')
}

// โหลดข้อมูลเมื่อ component ถูกโหลด
onMounted(() => {
  // ดึงข้อมูลจาก localStorage ก่อน
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      const parsedUser = JSON.parse(storedUser)
      user.value = {
        ...user.value,
        ...parsedUser,
        original_image_url: parsedUser.profile_image_url || ''
      }
      editForm.value = {
        username: parsedUser.username,
        email: parsedUser.email,
        profile_image: null
      }
    } catch (e) {
      console.error('Error parsing user data:', e)
    }
  }
  
  // ดึงข้อมูลล่าสุดจากเซิร์ฟเวอร์
  fetchUserProfile()
})
</script>
<template>
  <div class="min-h-screen bg-black text-white p-6 max-w-6xl mx-auto grid grid-cols-10 gap-8">
    <!-- ส่วนซ้าย -->
    <div class="col-span-7">
      <h1 class="text-3xl font-bold mb-6">👥 สมาชิกผู้จัดทำ</h1>
      <p class="text-gray-300 mb-6 leading-relaxed">
        พบกับทีมผู้พัฒนาที่อยู่เบื้องหลังแอป <span class="text-white font-semibold">Share Notes</span> ซึ่งสร้างขึ้นเพื่อให้ทุกคนสามารถแบ่งปันไอเดีย ความรู้ และแรงบันดาลใจร่วมกัน
      </p>

      <div class="space-y-6">
        <div
          v-for="member in teamMembers"
          :key="member.name"
          class="border border-gray-700 p-5 rounded-md bg-gray-900 flex items-center gap-6"
        >
          <img
            :src="member.image"
            alt="Member Photo"
            class="w-32 h-32 object-cover rounded-full border-2 border-gray-600"
          />
          <div class="flex-1">
            <h2 class="text-white font-semibold text-xl">{{ member.name }}</h2>
            <p class="text-gray-400 text-sm">{{ member.role }}</p>
            <div class="text-sm text-gray-500 mt-2 space-y-1">
              <div v-if="member.email">
                📧 <a :href="`mailto:${member.email}`" class="text-blue-400 hover:underline">{{ member.email }}</a>
              </div>
              <div v-if="member.github">
                🐙 <a :href="member.github" target="_blank" class="text-blue-400 hover:underline">{{ member.github }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ฝั่งขวา -->
    <div class="col-span-3 self-start mt-34">
      <div class="sticky top-24 bg-gray-900 border border-gray-700 rounded-md p-6">
        <h2 class="text-2xl font-bold mb-4">🛠️ เทคโนโลยีที่ใช้</h2>
        <ul class="space-y-3 text-gray-300 text-sm">
          <li>
            <span class="text-white font-semibold">Frontend:</span> Nuxt 3 (Vue 3), Tailwind CSS
          </li>
          <li>
            <span class="text-white font-semibold">CSS:</span> Tailwind CSS
          </li>
          <li>
            <span class="text-white font-semibold">Backend:</span> Python, Flask
          </li>
          <li>
            <span class="text-white font-semibold">Database:</span> MongoDB
          </li>
        </ul>

        <h3 class="text-xl font-semibold mt-6 mb-2">🔗 GitHub</h3>
        <a
          href="https://github.com/67319010002/miniproject"
          target="_blank"
          class="text-blue-400 hover:underline break-all"
        >
          github.com/67319010002/miniproject
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
const teamMembers = [
  {
    name: 'นางสาวชนิดาภา ลานนท์',
    role: 'นักพัฒนา Full-stack',
    email: '67319010002@loeitech.ac.th',
    github: 'https://github.com/67319010002',
    image: '/upload/frame.jpg', // ✅ รูปจากเครื่อง
  },
  {
    name: 'นายณัฐดนัย วรรณชัย',
    role: 'Backend Developer',
    email: '67319010005@loeitech.ac.th',
    github: 'https://github.com/67319010005',
    image: 'upload/pluem.jpg', // ✅ รูปจากเครื่อง
  },
  {
    name: 'นางสาวศิลป์ณวาริน ทีจันทา',
    role: 'UI/UX Designer',
    email: '67319010014@loeitech.ac.th',
    github: 'https://github.com/67319010014',
    image: 'upload/muay.jpg', // ✅ รูปจากเครื่อง
  },
  {
    name: 'นายธนวัฒน์ มาแสนจันทร์',
    role: 'Frontend Developer',
    email: '67319010035@loeitech.ac.th',
    github: 'https://github.com/67319010035',
    image: 'upload/benz.jpg', // ✅ รูปจากเครื่อง
  },
];
</script>

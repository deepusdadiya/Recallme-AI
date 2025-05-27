<template>
  <section class="bg-gradient-to-br from-indigo-50 to-white py-20 px-4 text-center">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-4xl sm:text-5xl font-extrabold text-gray-800 mb-6">
        🧠 Recallme-AI
      </h1>
      <p class="text-lg sm:text-xl text-gray-600 mb-8">
        Your personal AI memory vault — upload, recall, and ask from anything: notes, chats, voice memos, or screenshots.
      </p>
      <div class="flex justify-center gap-4">
        <router-link
          to="/login"
          class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg text-sm font-semibold shadow">
          🔐 Login
        </router-link>
        <a
          href="#features"
          class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-3 rounded-lg text-sm font-semibold border">
          🔍 Explore Features
        </a>
      </div>
    </div>
  </section>
</template>
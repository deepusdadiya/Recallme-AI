<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-black to-gray-900 text-white px-6 py-16">
    <div class="max-w-3xl mx-auto text-center text-white px-4">
    <h2 class="text-2xl sm:text-3xl font-bold text-pink-400 mb-4">
        🧠 Welcome to Recallme-AI
    </h2>

    <p class="text-xl sm:text-2xl text-white/80 font-medium leading-snug mb-6">
        Experience Limitless Memory Search with <span class="text-pink-300 font-semibold">Recallme-AI</span> — Your Thoughts, Forever Searchable
    </p>

    <p class="text-pink-200 text-base sm:text-lg italic leading-relaxed mb-4">
        Recallme-AI lets you upload and organize everything — screenshots, voice notes, PDFs, and ideas — and turns them into searchable, intelligent memories.
        Just drop your files in, and later ask anything like
        <span class="font-semibold">“What did I say about GPT-4 yesterday?”</span>
    </p>

    <p class="text-pink-200 text-base sm:text-lg italic leading-relaxed">
        Your memories become a <span class="font-semibold text-pink-300">personal knowledge base powered by AI</span>. Instantly extract insights, trace past conversations, and recall every important detail — across formats, moments, and topics.
    </p>
      <div class="mt-8 flex justify-center gap-6 mb-10">
        <router-link to="/upload">
          <button class="bg-pink-600 hover:bg-pink-700 text-white font-semibold px-6 py-3 rounded-full shadow transition duration-300">
            📁 Upload a Memory
          </button>
        </router-link>
        <router-link to="/query">
          <button class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-full shadow transition duration-300">
            💬 Ask a Question
          </button>
        </router-link>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
      <div class="bg-white/5 hover:bg-white/10 border border-white/20 rounded-2xl p-8 shadow-lg transition duration-300">
        <h3 class="text-xl font-bold mb-4">🔐 Secure Memory Vault</h3>
        <ul class="space-y-3 text-white/90 text-lg list-disc pl-5">
          <li>Your uploaded memories are end-to-end encrypted and stored securely in your personal vault.</li>
          <li>Indexed using semantic AI for faster, smarter retrieval.</li>
          <li>Only you can access and query your memories — total privacy ensured.</li>
        </ul>
      </div>

      <div class="bg-white/5 hover:bg-white/10 border border-white/20 rounded-2xl p-8 shadow-lg transition duration-300">
        <h3 class="text-xl font-bold mb-4">💡 Smart Memory Search</h3>
        <ul class="space-y-3 text-white/90 text-lg list-disc pl-5">
          <li>Ask natural questions about anything you've uploaded — from summaries to specific facts.</li>
          <li>AI reads and understands your files, returning the most relevant insights.</li>
          <li>Supports follow-up context and memory-linked conversation chains.</li>
        </ul>
      </div>

      <div class="bg-white/5 hover:bg-white/10 border border-white/20 rounded-2xl p-8 shadow-lg transition duration-300">
        <h3 class="text-xl font-bold mb-4">📊 Visual Dashboard (coming soon)</h3>
        <ul class="space-y-3 text-white/90 text-lg list-disc pl-5">
          <li>View your uploaded memories and answers visually as a knowledge graph.</li>
          <li>Drag, filter, and connect different chunks of memory and data points.</li>
          <li>Identify hidden patterns, relationships, and track memory insights over time.</li>
        </ul>
      </div>
    </div>

    <div class="mt-10 text-center text-white/80 text-lg max-w-3xl mx-auto">
      <p>
        Upload screenshots, audio notes, PDFs, and ask smart questions about your memories later.<br>
        Recallme-AI empowers you to create your own searchable, contextual knowledge base.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView'
}
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
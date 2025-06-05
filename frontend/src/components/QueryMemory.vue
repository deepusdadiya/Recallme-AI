<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-purple-900 to-black px-4">
    <div class="w-full max-w-2xl bg-white/5 border border-white/10 rounded-2xl shadow-lg p-8 text-white">
      <h2 class="text-2xl font-bold mb-6 text-center">🧠 Ask a Memory Question</h2>

      <form @submit.prevent="submitQuery" class="space-y-4">
        <input
          v-model="queryText"
          type="text"
          placeholder="e.g., What did I say about GPT-4 yesterday?"
          class="w-full bg-white/10 border border-white/20 text-white placeholder-white/60 px-4 py-3 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
          required
        />
        <button
          type="submit"
          class="w-full py-3 text-lg font-bold text-white bg-gradient-to-r from-pink-600 to-purple-600 rounded-xl hover:from-pink-700 hover:to-purple-700 transition-all shadow-md"
        >
          Ask
        </button>
      </form>

      <div v-if="answer" class="mt-8">
        <p class="text-pink-400 text-lg font-semibold mb-2">💡 Answer:</p>
        <div class="bg-white/10 border border-white/20 p-4 rounded-lg text-white/90 whitespace-pre-line">
          {{ answer }}
        </div>
      </div>

      <div v-if="matches.length" class="mt-8">
        <p class="text-white/80 text-lg font-semibold mb-2">📎 Matched Memory Chunks:</p>
        <ul class="space-y-3">
          <li
            v-for="match in matches"
            :key="match.metadata.memory_id"
            class="bg-white/10 border border-white/10 p-3 rounded-md text-white/80 text-sm whitespace-pre-line"
          >
            {{ match.content }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const queryText = ref('')
const answer = ref('')
const matches = ref([])

const submitQuery = async () => {
  const token = localStorage.getItem('token')

  try {
    const response = await axios.post(
      'http://localhost:8000/api/memory/query',
  {
    query: queryText.value.trim(),
    source_type: null,
    title: null,
    user_id: null
  },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    answer.value = response.data.answer
    matches.value = response.data.matches
  } catch (error) {
    answer.value = '❌ Error processing your query.'
    console.error(error)
  }
}
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
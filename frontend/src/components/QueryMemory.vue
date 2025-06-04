<template>
  <div class="bg-white/5 border border-white/20 rounded-xl p-6 w-full max-w-md text-white shadow-xl flex flex-col justify-between">
    <h2 class="text-lg font-semibold mb-4">🧠 Ask a Question</h2>

    <form @submit.prevent="submitQuery" class="space-y-4">
      <input
        v-model="queryText"
        type="text"
        placeholder="e.g., What did I discuss about project X?"
        class="w-full bg-white/10 border border-white/20 text-white placeholder-white/60 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400"
        required
      />
      <button
        type="submit"
        class="w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold px-4 py-2 rounded shadow"
      >
        Ask
      </button>
    </form>

    <div v-if="answer" class="mt-6">
      <p class="text-pink-300 font-semibold mb-2">💡 Answer:</p>
      <p class="text-white/90">{{ answer }}</p>
    </div>

    <div v-if="matches.length" class="mt-6">
      <p class="text-white/80 mb-2 font-semibold">📎 Matched Memory Chunks:</p>
      <ul class="space-y-2 text-sm">
        <li
          v-for="match in matches"
          :key="match.metadata.memory_id"
          class="bg-white/10 border border-white/10 p-3 rounded"
        >
          {{ match.content }}
        </li>
      </ul>
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
  const payload = {
    query: queryText.value.trim()
  }

  console.log("Sending query payload:", payload)

  try {
    const response = await axios.post(
      'http://localhost:8000/api/memory/query',
      payload,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    console.log("Response received:", response.data)

    answer.value = response.data.answer
    matches.value = response.data.matches
  } catch (error) {
    if (error.response) {
      console.error("Query error:", error)
      console.error("Status:", error.response.status)
      console.error("Data:", error.response.data)
    } else {
      console.error("Generic error:", error.message)
    }
  }
}
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
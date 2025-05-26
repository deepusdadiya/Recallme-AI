<template>
  <div class="bg-white rounded-lg shadow p-6 w-full max-w-xl">
    <h2 class="text-xl font-bold mb-4">🧠 Ask a Question</h2>
    <input
      v-model="query"
      placeholder="e.g., What did I discuss about project X?"
      class="border w-full p-2 rounded mb-4 text-sm"
    />
    <button
      @click="ask"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
      Ask
    </button>

    <div v-if="answer" class="mt-6">
      <p class="text-gray-700 mb-2 font-semibold">💡 Answer:</p>
      <div class="bg-gray-100 p-3 rounded text-sm">{{ answer }}</div>
    </div>

    <div v-if="matches.length" class="mt-6">
      <p class="text-gray-700 mb-2 font-semibold">📎 Matched Memory Chunks:</p>
      <ul class="space-y-2 text-sm">
        <li
          v-for="match in matches"
          :key="match.metadata.chunk_id"
          class="bg-blue-50 border p-3 rounded">
          {{ match.page_content }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { queryMemory } from '../api';

export default {
  data() {
    return {
      query: '',
      answer: '',
      matches: []
    };
  },
  methods: {
    async ask() {
      try {
        const res = await queryMemory(this.query);
        this.answer = res.data.answer;
        this.matches = res.data.matches;
      } catch (err) {
        this.answer = 'Error occurred while querying.';
        console.error(err);
      }
    }
  }
};
</script>
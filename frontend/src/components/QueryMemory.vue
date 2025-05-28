<template>
  <div class="bg-white/5 border border-white/20 rounded-xl p-6 w-full max-w-md text-white shadow-xl flex flex-col justify-between">
    <h2 class="text-lg font-semibold mb-4">🧠 Ask a Question</h2>

    <form @submit.prevent="submitQuery" class="space-y-4">
      <input
        v-model="query"
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
          :key="match.metadata.chunk_id"
          class="bg-white/10 border border-white/10 p-3 rounded"
        >
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
    async submitQuery() {
      try {
        const res = await queryMemory({ query: this.query });
        this.answer = res.data.answer;
        this.matches = res.data.matches || [];
        console.log("LLM response:", res.data);
      } catch (err) {
        this.answer = '❌ Something went wrong. Please try again.';
        this.matches = [];
        console.error('Query error:', err);
      }
    }
  }
};
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
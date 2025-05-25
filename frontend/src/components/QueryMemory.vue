<template>
  <div>
    <h2>Ask a Question</h2>
    <input v-model="query" placeholder="Ask something..." />
    <button @click="ask">Ask</button>
    <p v-if="answer"><strong>Answer:</strong> {{ answer }}</p>
    <div v-for="match in matches" :key="match.metadata.chunk_id" class="match">
      <p><strong>Match:</strong> {{ match.content }}</p>
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
        this.answer = 'Error occurred';
        console.error(err);
      }
    }
  }
};
</script>
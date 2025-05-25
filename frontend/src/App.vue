<template>
  <div id="app">
    <h1>🧠 Recallme-AI</h1>
    <UploadFile />
    <QueryMemory />
  </div>
</template>

<script>
import UploadFile from './components/UploadFile.vue';
import QueryMemory from './components/QueryMemory.vue';

export default {
  components: { UploadFile, QueryMemory }
};
</script>
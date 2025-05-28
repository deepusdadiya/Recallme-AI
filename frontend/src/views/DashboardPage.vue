<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-black to-gray-900 text-white px-6 py-10">
    <h1 class="text-3xl font-extrabold text-center text-pink-400 mb-10">
      🧠 Welcome to Recallme-AI
    </h1>

    <div class="flex flex-col lg:flex-row gap-8 justify-center items-start max-w-6xl mx-auto">
      <!-- Wrap UploadFile only, since it doesn't have its own card -->
      <div class="bg-white/10 border border-white/20 rounded-2xl p-6 w-full max-w-md shadow-lg">
        <UploadFile />
      </div>

      <!-- No outer div here — QueryMemory already has card styling -->
      <QueryMemory />
    </div>
  </div>
</template>

<script>
import UploadFile from '../components/UploadFile.vue';
import QueryMemory from '../components/QueryMemory.vue';

export default {
  components: {
    UploadFile,
    QueryMemory
  }
};
</script>
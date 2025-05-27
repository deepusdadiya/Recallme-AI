<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-100 to-white p-6">
    <h1 class="text-3xl font-bold text-center text-indigo-800 mb-8">Welcome to Your Dashboard 🧠</h1>
    <div class="flex flex-col lg:flex-row gap-8 justify-center items-start max-w-7xl mx-auto">
      <UploadFile />
      <QueryMemory />
    </div>
  </div>
</template>

<script>
import UploadFile from '../components/UploadFile.vue'
import QueryMemory from '../components/QueryMemory.vue'

export default {
  components: {
    UploadFile,
    QueryMemory
  }
}
</script>
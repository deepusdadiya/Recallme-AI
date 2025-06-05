<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-purple-900 to-black px-4">
    <div class="w-full max-w-md bg-white/5 p-8 rounded-2xl border border-white/10 shadow-lg">
      <h2 class="text-2xl font-bold text-white text-center mb-6">🧠 Upload a Memory</h2>

      <input
        type="file"
        @change="handleFile"
        class="block w-full text-sm text-white bg-transparent border border-white/30 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-pink-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-pink-600 file:text-white hover:file:bg-pink-700"
      />

      <button
        @click="submitFile"
        class="w-full mt-6 py-3 text-lg font-bold text-white bg-gradient-to-r from-pink-600 to-purple-600 rounded-xl hover:from-pink-700 hover:to-purple-700 transition-all shadow-md"
      >
        Upload
      </button>

      <p v-if="message" :class="`mt-4 text-sm font-medium ${messageColorClass}`">
        {{ message }}
      </p>
      <p class="text-white/60 text-sm mt-2">
        Supported formats: PDF, DOCX, TXT, JPG, PNG
      </p>
      <p v-if="loading" class="text-pink-400 mt-4">⏳ Uploading...</p>
      <p v-if="error" class="text-red-400 mt-4">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { uploadFile } from '../api';

export default {
  data() {
    return {
      file: null,
      message: '',
      messageColorClass: '',
      loading: false,
      error: ''
    };
  },
  methods: {
    handleFile(e) {
      this.file = e.target.files[0];
    },
    async submitFile() {
      if (!this.file) {
        this.message = '❗Please select a file first.';
        this.messageColorClass = 'text-yellow-400';
        return;
      }

      this.loading = true;
      this.error = '';
      this.message = '';

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const res = await uploadFile(formData);
        if (res.status === 200 && res.data.status === 'success') {
          this.message = '✅ Upload successful!';
          this.messageColorClass = 'text-green-400';
        } else {
          this.message = '⚠️ Upload may have failed.';
          this.messageColorClass = 'text-yellow-400';
        }
      } catch (err) {
        this.error = '❌ Upload failed. Check console for details.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
</style>
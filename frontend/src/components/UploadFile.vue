<template>
  <div class="space-y-4">
    <h2 class="text-lg font-bold text-white mb-2">🗂️ Upload Memory</h2>
    <input
      type="file"
      @change="handleFile"
      class="bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-pink-400 rounded px-3 py-2 w-full"
    />
    <button
      @click="submitFile"
      class="bg-pink-600 hover:bg-pink-700 text-white font-semibold px-4 py-2 rounded shadow w-full"
    >
      Upload
    </button>
    <p v-if="message" :class="`text-sm mt-2 text-${messageColor}-400`">{{ message }}</p>
  </div>
</template>

<script>
import { uploadFile } from '../api';

export default {
  data() {
    return {
      file: null,
      message: '',
      messageColor: ''
    };
  },
  methods: {
    handleFile(e) {
      this.file = e.target.files[0];
    },
    async submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const res = await uploadFile(formData);
        if (res.status === 200 && res.data.status === 'success') {
          this.message = '✅ Upload successful!';
          this.messageColor = 'green';
        } else {
          this.message = '⚠️ Upload may have failed.';
          this.messageColor = 'yellow';
        }
      } catch (err) {
        this.message = '❌ Upload failed.';
        this.messageColor = 'red';
        console.error(err);
      }
    }
  }
};
</script>
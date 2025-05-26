<template>
  <div class="bg-white rounded-lg shadow p-6 w-full max-w-md">
    <h2 class="text-xl font-bold mb-4">📂 Upload Memory</h2>
    <input type="file" @change="handleFile" class="block w-full text-sm text-gray-700 mb-4" />
    <button
      @click="submitFile"
      class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition">
      Upload
    </button>

    <p v-if="message" class="mt-4 text-sm" :class="{
      'text-green-600': messageColor === 'green',
      'text-red-600': messageColor === 'red',
      'text-orange-600': messageColor === 'orange'
    }">
      {{ message }}
    </p>
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
      if (!this.file) return;
      const formData = new FormData();
      formData.append('file', this.file);

    try {
    const res = await uploadFile(formData);
    console.log("Upload response:", res);
    const status = res?.data?.status || null;
    if (status === 'success') {
        this.message = '✅ Upload successful!';
        this.messageColor = 'green';
    } else {
        this.message = '⚠️ Upload may have failed.';
        this.messageColor = 'orange';
    }
    } catch (err) {
    this.message = '❌ Upload failed.';
    this.messageColor = 'red';
    console.error("Upload error:", err);
    }
    }
  }
};
</script>
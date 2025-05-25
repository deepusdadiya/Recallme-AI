<template>
  <div>
    <h2>Upload Memory</h2>
    <input type="file" @change="handleFile" />
    <button @click="submitFile">Upload</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import { uploadFile } from '../api';

export default {
  data() {
    return {
      file: null,
      message: ''
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
        this.message = 'Uploaded successfully!';
      } catch (err) {
        this.message = 'Upload failed.';
        console.error(err);
      }
    }
  }
};
</script>
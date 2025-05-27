<template>
  <div class="min-h-screen bg-gradient-to-b from-sky-100 to-white flex items-center justify-center">
    <div class="bg-white shadow-2xl rounded-2xl p-10 w-full max-w-md border border-gray-200">
      <h2 class="text-2xl font-bold text-gray-800 text-center mb-6">Welcome to Recallme-AI</h2>
      <form @submit.prevent="submitLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-600">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="mt-1 block w-full px-4 py-2 border rounded-xl shadow-sm focus:ring focus:outline-none focus:ring-blue-300"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-600">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="mt-1 block w-full px-4 py-2 border rounded-xl shadow-sm focus:ring focus:outline-none focus:ring-blue-300"
            placeholder="Enter your password"
          />
        </div>

        <div class="flex justify-between items-center">
          <div class="text-sm">
            <a href="#" class="text-blue-500 hover:underline">Forgot password?</a>
          </div>
        </div>

        <button
          type="submit"
          class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          Log In
        </button>

        <p v-if="errorMessage" class="text-red-500 text-sm text-center">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async submitLogin() {
      try {
        const res = await axios.post('http://localhost:8000/api/auth/login', {
          email: this.email,
          password: this.password,
        });

        if (res.data.status === 'Login successful') {
          // Store user_id or token as needed
          alert('✅ Login success!');
          this.errorMessage = '';
          // Redirect or update state
          this.$router.push('/dashboard');
        }
      } catch (err) {
        this.errorMessage = 'Login failed. Please check your credentials or verify your email.';
        console.error(err);
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
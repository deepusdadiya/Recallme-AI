<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-black to-gray-900 flex items-center justify-center text-white">
    <div class="bg-black bg-opacity-40 shadow-2xl rounded-2xl p-10 w-full max-w-md border border-gray-800">
      <h2 class="text-2xl font-bold text-pink-400 text-center mb-6">Create Your Recallme-AI Account</h2>

      <form @submit.prevent="submitSignup" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-300">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-xl shadow-sm focus:ring focus:outline-none focus:ring-pink-400"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-300">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="mt-1 block w-full px-4 py-2 border border-gray-700 bg-gray-800 text-white rounded-xl shadow-sm focus:ring focus:outline-none focus:ring-pink-400"
            placeholder="Create a secure password"
          />
        </div>

        <button
          type="submit"
          class="w-full py-2 px-4 bg-pink-700 hover:bg-pink-800 text-white font-semibold rounded-xl shadow focus:outline-none focus:ring-2 focus:ring-pink-400"
        >
          Sign Up
        </button>

        <p class="mt-4 text-sm text-center">
          Already have an account?
          <router-link to="/login" class="text-blue-400 hover:underline">Log In</router-link>
        </p>

        <p v-if="errorMessage" class="text-red-400 text-sm text-center">{{ errorMessage }}</p>
      </form>
    </div>

    <!-- ✅ Success toast at bottom -->
    <div
      v-if="showToast"
      class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-6 py-2 rounded shadow-lg z-50 transition-opacity duration-300"
    >
      ✅ Signup successful! Please verify your email.
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
      errorMessage: '',
      showToast: false
    };
  },
  methods: {
    async submitSignup() {
      try {
        await axios.post('http://localhost:8000/api/auth/signup', {
          email: this.email,
          password: this.password
        });

        this.errorMessage = '';
        this.showToast = true;

        setTimeout(() => {
          this.showToast = false;
          this.$router.push('/login');
        }, 1500);
      } catch (err) {
        this.errorMessage = err.response?.data?.detail || 'Signup failed. Please try again.';
        console.error(err);
      }
    }
  }
};
</script>
<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-black to-gray-900 text-white px-8 py-16">
  <div class="max-w-7xl mx-auto flex flex-col-reverse lg:flex-row items-center justify-between gap-12 h-full">
    <!-- ... Left and Right Content ... -->
           <!-- LEFT: Text Content -->
      <div class="text-left flex-1">
        <h1 class="text-4xl lg:text-6xl font-extrabold leading-tight text-pink-400">
          Build Your AI Memory<br />
          Vault
        </h1>
        <p class="mt-6 text-lg text-gray-300 max-w-xl">
          Upload screenshots, voice notes, or PDF ideas — then just ask anything later like<br />
          <span class="italic text-white">“What did I say about GPT-4 yesterday?”</span>
        </p>
        <div class="mt-8 flex gap-4">
          <router-link to="/login">
            <button class="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-full font-semibold">
              Get Started
            </button>
          </router-link>
          <router-link to="/dashboard">
            <button class="bg-white text-black px-6 py-3 rounded-full font-semibold hover:bg-gray-200">
              Explore Demo
            </button>
          </router-link>
        </div>
      </div>

      <!-- RIGHT: Image -->
    <div class="flex-1 h-[80vh] flex items-center justify-center">
        <img
          src="/src/assets/orbit-graphic.png"
          alt="Futuristic AI Brain"
          class="w-full max-w-lg h-[650px] object-contain lg:h-[600px]"
        />
    </div>
  </div>
</div>
</template>
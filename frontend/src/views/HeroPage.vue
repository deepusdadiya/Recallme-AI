<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-black to-gray-900 text-white">
    <div class="container-fluid h-screen">
      <div class="row h-100">
        <!-- LEFT SIDE -->
        <div class="col-lg-5 d-flex align-items-center">
          <div class="flex-1 flex flex-col justify-center space-y-6 px-4">
            <h1 class="text-4xl md:text-5xl font-extrabold text-pink-400">
              Build Your AI Memory Vault
            </h1>
            <p class="text-lg text-gray-300 max-w-md">
              Upload screenshots, voice notes, or PDF ideas — then just ask anything later like
              <em class="block mt-2 text-sm text-pink-200">"What did I say about GPT-4 yesterday?"</em>
            </p>
            <div class="flex space-x-4">
                <router-link to="/login">
                <button class="bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-6 rounded-full">
                    Get Started
                </button>
                </router-link>
              <button class="bg-white text-gray-900 hover:bg-gray-200 font-semibold py-2 px-6 rounded-full">
                Explore Demo
              </button>
            </div>
          </div>
        </div>

        <!-- RIGHT SIDE -->
        <div class="col-lg-7 p-0">
          <div class="h-100 w-100 d-flex align-items-center justify-content-center">
            <img
              src="/src/assets/image-trans.png"
              alt="AI Memory Visual"
              class="w-100 h-100 object-contain p-4"
              style="object-fit: contain"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
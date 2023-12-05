<template>
  <div>
    <h3>Login</h3>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useUserStore } from '../store/userStore';
import { useRouter } from 'vue-router';

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');

    const login = async () => {
      try {
        await userStore.login(username.value, password.value);
        if (userStore.isLoggedIn) {
          router.push({ name: 'Main Page' });
        } else {
          errorMessage.value = 'Login failed';
        }
      } catch (error) {
        console.error('Error during login:', error);
        errorMessage.value = 'Login failed. Please try again.';
      }
    };

    return { username, password, login, errorMessage };
  },
});
</script>
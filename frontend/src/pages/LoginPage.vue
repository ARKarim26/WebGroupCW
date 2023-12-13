<template>
  <div class="container mt-5">
    <h3>Login</h3>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" class="form-control" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" class="form-control" v-model="password" required>
      </div>
      <br>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>


<script lang="ts">
  import { defineComponent, ref } from "vue";
  import { useRouter } from "vue-router";
  import { useUserStore } from "../store/userStore";  // Adjust the path as per your project structure

  export default defineComponent({
    setup() {
      const router = useRouter();
      const userStore = useUserStore();  // Added
      const username = ref('');
      const password = ref('');

      const login = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: username.value,
              password: password.value
            })
          });

          if (response.ok) {
            userStore.isLoggedIn = true;  // Update login state
            router.push({ name: 'Main Page' });
          } else {
            console.error('Login failed: ', response.status, response.statusText);
            // Handle login failure
          }
        } catch (error) {
          console.error('Error:', error);
        }
      };

      return { username, password, login };
    },
  });
</script>



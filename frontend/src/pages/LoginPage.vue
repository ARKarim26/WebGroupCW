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
    </form>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";

  export default defineComponent({
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });

          if (response.ok) {
            console.log('Login successful');
            this.$router.push({ name: 'Main Page' });
          } else {
            console.error('Login failed: ', response.status, response.statusText);
            // Handle login failure
          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
    },
  });
</script>

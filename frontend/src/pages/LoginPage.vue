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
                  title: "Login Page",
                  username: "",
                  password: "",
              }
          },
          methods: {
          async login() {
            try {
              const response = await fetch('/login/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                  'username': this.username,
                  'password': this.password
                })
              });

        if (response.ok) {
          this.$router.push({ name: 'Main Page' });
        } else {
          console.error('Login failed');
          // Handle login failure
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
      })
  </script>
  
  <style scoped>
  .login-container {
    max-width: 300px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  label {
    font-weight: bold;
  }
  </style>
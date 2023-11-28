<template>
    <br>
    <div class="signup-container">
      <div class="h3">
        {{ title }}
      </div>
      <form @submit.prevent="handleSubmit">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>

        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>

        <label for="firstname">First Name:</label>
        <input type="text" id="fname" v-model="fname" required>

        <label for="lastname">First Name:</label>
        <input type="text" id="lname" v-model="lname" required>

        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
  
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>

        <label for="birthdate"> Birthday</label>
        <input type="date" id="birthdate" v-model="birthdate" required />

        <label for="categories"> Favourite Categories </label>
        <input type="text" id="categories" v-model="categories" required/> 

  
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    data() {
      return {
        title: "Signup Page",
        username: "",
        fname: "",
        lname: "",
        email: "",
        password: "",
        birthdate:"",
        categories:[],
      };
    },
    methods: {
      handleSubmit() {
        // Add your signup logic here
        console.log("Signing up with:", this.username, this.email, this.password);
        // You can send a request to your server or perform any other signup actions
      },
    },
  });
  </script>
  
  <style scoped>
  .signup-container {
    max-width: 400px;
    margin: 0 auto;
  }
  
  form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  label {
    font-weight: bold;
  }
  
  button {
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  
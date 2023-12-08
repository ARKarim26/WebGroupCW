<template>
  <div class="register-container">
    <h1>Register</h1>
    <form @submit.prevent="registerUser">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" placeholder="Username" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" placeholder="Password" required />
      </div>
      <div>
        <label for="passwordConfirm">Confirm Password</label>
        <input type="password" id="passwordConfirm" v-model="passwordConfirm" placeholder="Confirm Password" required />
      </div>
      <div>
        <label for="birthDate">Birth Date</label>
        <input type="date" id="birthDate" v-model="birthDate" />
      </div>
      <div>
        <label for="profileImage">Profile Image</label>
        <input type="file" id="profileImage" @change="onFileChange" />
      </div>
      <button type="submit">Register</button>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      username: '',
      password: '',
      passwordConfirm: '',
      birthDate: '',
      profileImage: null as File | null,
      errorMessage: '',
    };
  },
  methods: {
    onFileChange(e: Event) {
      const input = e.target as HTMLInputElement;
      if (!input.files) return;
      this.profileImage = input.files[0];
    },
    registerUser() {
      if (this.password !== this.passwordConfirm) {
        this.errorMessage = "Passwords do not match";
        return;
      }
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('password', this.password);
      formData.append('birth_date', this.birthDate);
      if (this.profileImage) {
        formData.append('profile_image', this.profileImage, this.profileImage.name);
      }
      fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || 'Registration failed. Please try again.');
          });
        }
        return response.json();
      })
      .then(() => this.$router.push('/login'))
      .catch((error) => this.errorMessage = error.message);
    }
  }
});
</script>

<style scoped>
/* Your CSS styles */
</style>

  
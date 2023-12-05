<template>
  <div class="profile-container">
    <h1>Profile Page</h1>
    <div v-if="userStore.isLoggedIn">
      <form @submit.prevent="updateProfile">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" id="email">
        </div>
        <div>
          <label for="birthDate">Birth Date:</label>
          <input type="date" v-model="birthDate" id="birthDate">
        </div>
        <div>
          <label for="profileImage">Profile Image:</label>
          <input type="file" @change="handleFileChange" id="profileImage">
        </div>
        <button type="submit">Update Profile</button>
      </form>
      <button @click="logout">Logout</button>
    </div>
    <div v-else>
      <p>Please <router-link to="/login">login</router-link> to view your profile.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../store/userStore';

export default defineComponent({
  setup() {
    const router = useRouter();
    const userStore = useUserStore();
    const email = ref(userStore.email);
    const birthDate = ref(userStore.birthDate);
    const profileImage = ref(userStore.profileImage);

    const fetchProfile = async () => {
      // Fetch user profile data from the backend
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', { credentials: 'include' });
        if (!response.ok) throw new Error('Failed to fetch profile');
        const data = await response.json();
        userStore.setUserProfile(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const updateProfile = async () => {
      // Update user profile in the backend
      const formData = new FormData();
      formData.append('email', email.value);
      formData.append('birth_date', birthDate.value);
      // Handle file upload for profile image
      // ...

      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', {
          method: 'POST',
          body: formData,
          credentials: 'include'
        });
        if (!response.ok) throw new Error('Failed to update profile');
        // Update local store with new profile data
        // ...
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const handleFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files[0]) {
        profileImage.value = URL.createObjectURL(input.files[0]);
        // You might want to update the profile image in the store or send it to the backend
      }
    };

    const logout = () => {
      userStore.logoutUser();
      router.push('/');
    };

    onMounted(fetchProfile);

    return { email, birthDate, profileImage, updateProfile, handleFileChange, logout, userStore };
  },
});
</script>


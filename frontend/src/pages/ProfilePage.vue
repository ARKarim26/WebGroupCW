<template>
  <div class="profile-container">
    <h1>Profile Page</h1>
    <div v-if="userStore.isLoggedIn">
      <h2>My Details</h2>
      <p>Email: {{ userStore.email }}</p>
      <p>Birth Date: {{ userStore.birthDate }}</p>
      <img v-if="userStore.profileImage" :src="userStore.profileImage" alt="Current Profile Image" />
      <p>Favorite Categories: {{ userStore.favoriteCategories.join(', ') }}</p>

      <h2>Update Details</h2>
      <form @submit.prevent="updateProfile">
        <div>
          <label for="email">New Email:</label>
          <input type="email" v-model="email" id="email">
        </div>
        <div>
          <label for="birthDate">New Birth Date:</label>
          <input type="date" v-model="birthDate" id="birthDate">
        </div>
        <div>
          <label for="profileImage">New Profile Image:</label>
          <input type="file" @change="handleFileChange" id="profileImage">
          <img v-if="profileImageUrl" :src="profileImageUrl" alt="New Profile Image" />
        </div>
        <!-- Add favorite categories update logic here -->
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
    const userStore = useUserStore();
    const router = useRouter();
    const email = ref('');
    const birthDate = ref('');
    const profileImageInput = ref<File | null>(null);
    const profileImageUrl = ref('');

    const fetchProfile = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) throw new Error('Failed to fetch profile data');
        const profileData = await response.json();

        userStore.setUserProfile({
          username: profileData.username,
          email: profileData.email,
          birthDate: profileData.birth_date,
          profileImage: profileData.profile_image,
          favoriteCategories: profileData.favorite_categories,
        });

        email.value = profileData.email;
        birthDate.value = profileData.birth_date;
        profileImageUrl.value = profileData.profile_image;
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const handleFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input && input.files && input.files[0]) {
        profileImageInput.value = input.files[0];
        profileImageUrl.value = URL.createObjectURL(input.files[0]);
      }
    };

    const updateProfile = async () => {
      const formData = new FormData();
      formData.append('email', email.value);
      formData.append('birth_date', birthDate.value);
      if (profileImageInput.value) {
        formData.append('profile_image', profileImageInput.value);
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) throw new Error('Failed to update profile');
        const updatedUserData = await response.json();
        userStore.setUserProfile(updatedUserData);
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    };

    const logout = () => {
      userStore.logoutUser();
      router.push('/');
    };

    onMounted(fetchProfile);

    return {
      email, birthDate, profileImageInput, profileImageUrl, updateProfile, handleFileChange, logout, userStore
    };
  },
});
</script>

<style scoped>
/* Your CSS styles */
</style>
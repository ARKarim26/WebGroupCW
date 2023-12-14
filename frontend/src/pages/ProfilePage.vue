<template>
  <div class="container profile-container mt-5">
  <div class="profile-container">
    <h1 class="mb-4">Profile Page</h1>
    <div v-if="userStore.isLoggedIn">
      <div class="card">
        <div class="card-body">
          <h2 class="card-title">My Details</h2>
          <p class="card-text"><strong>Email:</strong> {{ email }}</p>
          <p class="card-text"><strong>Birth Date:</strong> {{ birthDate }}</p>
          
          <img v-if="profileImageUrl" :src="profileImageUrl" alt="Current Profile Image" class="img-fluid mb-3" />

          <h2 class="card-title">Update Details</h2>
          
          <form @submit.prevent="updateProfile">
            <div class="form-group">
              <label for="email">New Email:</label>
              <input type="email" v-model="email" id="email" class="form-control">
            </div>
            <br>
            <div class="form-group">
              <label for="birthDate">New Birth Date:</label>
              <input type="date" v-model="birthDate" id="birthDate" class="form-control">
            </div>
            <br>
            <div class="form-group">
              <label for="profileImage">New Profile Image: &nbsp</label>
              <input type="file" @change="handleFileChange" id="profileImage" class="form-control-file">
          
              <img v-if="profileImageUrl" :src="profileImageUrl" alt="New Profile Image"  class="img-fluid mt-3" />
            </div>
            <br>
         <div class="form-group">
              <label for="favoriteCategories">Favorite Categories:</label>
              <select id="favoriteCategories" v-model="selectedCategories" multiple class="form-control">
                <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <br>
        <button type="submit" class="btn btn-primary">Update Profile</button>
      </form>
      <button @click="logout" class="btn btn-danger mt-3">Logout</button>
    </div>
  </div>
</div>
<div v-else>
  <p>Please <router-link to="/login">login</router-link> to view your profile.</p>
</div>
</div>
</div>

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../store/userStore';

interface Category {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const username = ref('');
    const email = ref('');
    const birthDate = ref('');
    const profileImageInput = ref<File | null>(null);
    const profileImageUrl = ref('');
    const categories = ref<Category[]>([]);
    const selectedCategories = ref<number[]>([]);

    onMounted(async () => {
      await fetchProfile();
      await fetchCategories();
    });

    const fetchProfile = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        });

        if (!response.ok) throw new Error('Failed to fetch profile data');
        const profileData = await response.json();

        username.value = profileData.username;
        email.value = profileData.email;
        birthDate.value = profileData.birth_date;
        profileImageUrl.value = profileData.profile_image;
        selectedCategories.value = profileData.favorite_categories;
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const fetchCategories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/categories/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        });

        if (!response.ok) throw new Error('Failed to fetch categories');
        const data = await response.json();
        categories.value = data;
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
      selectedCategories.value.forEach(categoryId => {
        formData.append('favorite_categories', categoryId.toString());
      });

      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', {
          method: 'POST',
          body: formData,
          credentials: 'include',
        });

        if (!response.ok) throw new Error('Failed to update profile');
        // Update the store with new user data
        const updatedUserData = await response.json();
        userStore.setUserProfile(updatedUserData);
        alert('Profile updated successfully');
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    };

    const logout = () => {
      userStore.logoutUser();
      router.push('/');
    };

    return {
      username, email, birthDate, profileImageInput, profileImageUrl, updateProfile, handleFileChange, logout, userStore, categories, selectedCategories
    };
  },
});
</script>

<style scoped>
/* Your CSS styles */
</style>




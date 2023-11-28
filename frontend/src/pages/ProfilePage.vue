<!-- ProfilePage.vue -->

<template>
    <div>
      <div class="h3">My Profile</div>
  
      <div v-if="loading">Loading...</div>
  
      <div v-else>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="profile.email" />
        </div>
  
        <div>
          <label for="birthDate">Birth Date:</label>
          <input type="date" id="birthDate" v-model="profile.birth_date" />
        </div>
  
        <div>
          <label for="profileImage">Profile Image:</label>
          <input type="file" id="profileImage" @change="handleImageChange" />
          <img v-if="profile.profile_image" :src="profile.profile_image" alt="Profile Image" />
        </div>
  
        <div>
          <label>Favorite Categories:</label>
          <select multiple v-model="selectedCategories">
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
  
        <button @click="updateProfile">Update Profile</button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  interface UserProfile {
    email: string;
    birth_date: string | null;
    profile_image: string | null;
    favorite_categories: number[];
  }
  
  export default defineComponent({
    data() {
      return {
        loading: true,
        profile: {
          email: "",
          birth_date: null,
          profile_image: null,
          favorite_categories: [] as number[],
        } as UserProfile,
        selectedCategories: [] as number[],
        categories: [] as { id: number; name: string }[],
      };
    },
    mounted() {
      // Fetch user profile data on component mount
      this.fetchProfile();
    },
    methods: {
      fetchProfile() {
        // Make a GET request to your API endpoint to fetch user profile data
        // Update the URL with the correct endpoint
        fetch("/api/user_profile/")
          .then((response) => response.json())
          .then((data: UserProfile) => {
            this.profile = data;
            this.selectedCategories = data.favorite_categories;
            this.loading = false;
          })
          .catch((error) => console.error("Error fetching profile:", error));
      },
      handleImageChange() {
        // 
      },
      updateProfile() {
        // Update the URL with the correct endpoint
        fetch("http://localhost:8000/api/user/profile/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.profile.email,
            birth_date: this.profile.birth_date,
            favorite_categories: this.selectedCategories,
            // Add other fields as needed
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Profile updated successfully:", data.message);
            // Optionally, you can update the UI or show a success message
          })
          .catch((error) => console.error("Error updating profile:", error));
      },
    },
  });
  </script>
  
  <style scoped>

  </style>

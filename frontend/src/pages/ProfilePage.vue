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
    this.fetchProfile();
    this.fetchCategories();
  },
  methods: {
    fetchProfile() {
      fetch("/api/user/profile/")
        .then((response) => response.json())
        .then((data: UserProfile) => {
          this.profile = data;
          this.selectedCategories = data.favorite_categories;
          this.loading = false;
        })
        .catch((error) => console.error("Error fetching profile:", error));
    },
    fetchCategories() {
      fetch("/api/categories/")
        .then((response) => response.json())
        .then((data) => {
          this.categories = data.categories;
        })
        .catch((error) => console.error("Error fetching categories:", error));
    },
    handleImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('profile_image', file);

        fetch('/api/user/profile/', {
          method: 'POST',
          body: formData,
          credentials: 'include',
        })
        .then(response => response.json())
        .then(data => {
          if (data.profile_image) {
            this.profile.profile_image = data.profile_image;
          }
        })
        .catch(error => {
          console.error("Error uploading image:", error);
        });
      }
    },
    updateProfile() {
      const updatedData = {
        email: this.profile.email,
        birth_date: this.profile.birth_date,
        favorite_categories: this.selectedCategories,
      };

      fetch("/api/user/profile/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
        credentials: 'include',
      })
      .then((response) => response.json())
      .then((data) => {
        console.log("Profile updated successfully:", data.message);
      })
      .catch((error) => console.error("Error updating profile:", error));
    },
  },
});
</script>

  
<style scoped>
</style>

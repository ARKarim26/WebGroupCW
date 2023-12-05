<template>
  <div v-if="userStore.isLoggedIn">
    <h1>Profile</h1>
    <p>Username: {{ userStore.userData.username }}</p>
    <p>Email: {{ userStore.userData.email }}</p>
    <p>Birth Date: {{ userStore.userData.birthDate }}</p>
    <img v-if="userStore.userData.profileImage" :src="userStore.userData.profileImage" alt="Profile Image">
    <button @click="logout">Logout</button>
  </div>
  <div v-else>
    <p>You are not logged in.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '@/store/userStore';

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    userStore.fetchUserProfile();

    const logout = async () => {
      await fetch('http://127.0.0.1:8000/api/logout/', { method: 'POST' });
      userStore.logOut();
    };

    return { userStore, logout };
  },
});
</script>

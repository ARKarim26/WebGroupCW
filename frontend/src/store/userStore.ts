import { defineStore } from 'pinia';

interface User {
  username: string;
  email: string;
  birthDate?: string;
  profileImage?: string;
}

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    userData: null as User | null,
  }),
  actions: {
    logIn(userData: User) {
      this.isLoggedIn = true;
      this.userData = userData;
    },
    logOut() {
      this.isLoggedIn = false;
      this.userData = null;
    },
    async fetchUserProfile() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/');
        if (!response.ok) throw new Error('Failed to fetch user profile');
        const data = await response.json();
        this.logIn(data);
      } catch (error) {
        console.error('Error:', error);
      }
    }
  },
});

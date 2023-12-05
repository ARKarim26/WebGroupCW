import { defineStore } from 'pinia';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    username: '',
    email: '',
    birthDate: '',
    profileImage: '',
    favoriteCategories: [] as number[],
    isLoggedIn: false
  }),
  actions: {
    setUserProfile(userData: { username: string, email: string, birthDate: string, profileImage: string, favoriteCategories: number[] }) {
      this.username = userData.username;
      this.email = userData.email;
      this.birthDate = userData.birthDate;
      this.profileImage = userData.profileImage;
      this.favoriteCategories = userData.favoriteCategories;
    },
    loginUser(userData: { username: string, email: string, birthDate: string, profileImage: string, favoriteCategories: number[] }) {
      this.setUserProfile(userData);
      this.isLoggedIn = true;
    },
    logoutUser() {
      this.$reset(); // Resets the store to its initial state
    }
  }
});

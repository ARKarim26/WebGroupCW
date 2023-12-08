import { defineStore } from 'pinia';

interface UserProfile {
  username: string;
  email: string;
  birthDate: string;
  profileImage: string;
  favoriteCategories: number[];
}

interface UserState {
  username: string;
  email: string;
  birthDate: string;
  profileImage: string;
  favoriteCategories: number[];
  isLoggedIn: boolean;
}

export const useUserStore = defineStore('userStore', {
  state: (): UserState => ({
    username: '',
    email: '',
    birthDate: '',
    profileImage: '',
    favoriteCategories: [],
    isLoggedIn: false,
  }),
  actions: {
    setUserProfile(userData: UserProfile) {
      this.username = userData.username;
      this.email = userData.email;
      this.birthDate = userData.birthDate;
      this.profileImage = userData.profileImage;
      this.favoriteCategories = userData.favoriteCategories;
    },
    loginUser(userData: UserProfile) {
      this.setUserProfile(userData);
      this.isLoggedIn = true;
    },
    logoutUser() {
      this.$reset(); // Resets the store to its initial state
    },
    async updateProfile(formData: FormData) {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/profile/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Failed to update profile');
        }

        const updatedUserData: UserProfile = await response.json();
        this.setUserProfile(updatedUserData);
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
  },
});

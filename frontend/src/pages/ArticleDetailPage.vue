<template>
    <div v-if="article.data">
      <h2>{{ article.data.title }}</h2>
      <p>{{ article.data.content }}</p>
      <h3>Comments</h3>
      <ul>
        <li v-for="comment in article.data.comments" :key="comment.id">
          {{ comment.content }} - by {{ comment.author }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Article not found or loading...</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, reactive } from 'vue';
  import { useRoute } from 'vue-router';
  
  interface Article {
    id: number;
    title: string;
    content: string;
    author: string;
    comments: Comment[];
  }
  
  interface Comment {
    id: number;
    content: string;
    author: string;
  }
  
  export default defineComponent({
    setup() {
      const route = useRoute();
      const article = reactive<{ data: Article | null }>({ data: null });
  
      const fetchArticle = async () => {
        try {
          const response = await fetch(`/api/articles/${route.params.id}/`);
          if (!response.ok) throw new Error('Failed to fetch article');
          const data = await response.json();
          article.data = data;
        } catch (error) {
          console.error('Error:', error);
        }
      };
  
      onMounted(fetchArticle);
  
      return { article };
    },
  });
  </script>
  
  <style scoped>
  h3 {
    margin-top: 2rem;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 0.5rem 0;
  }
  </style>
  
<template>
    <div>
      <h2>Articles</h2>
      <div v-for="(articles, category) in categorizedArticles" :key="category">
        <h3>{{ category }}</h3>
        <ul>
          <li v-for="article in articles" :key="article.id">
            {{ article.title }} - by {{ article.author_name }}
            <router-link :to="`/articles/${article.id}`">
              <button>View</button>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, reactive } from 'vue';
  
  interface Article {
    id: number;
    title: string;
    author_name: string;
    category__name: string;
  }
  
  export default defineComponent({
    setup() {
      const categorizedArticles = reactive<Record<string, Article[]>>({});
  
      const fetchArticles = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/articles/');
          if (!response.ok) throw new Error('Failed to fetch articles');
          const data = await response.json();
          const articles: Article[] = data.articles;
  
          // Group articles by category
          articles.forEach(article => {
            if (!categorizedArticles[article.category__name]) {
              categorizedArticles[article.category__name] = [];
            }
            categorizedArticles[article.category__name].push(article);
          });
        } catch (error) {
          console.error('Error:', error);
        }
      };
  
      onMounted(fetchArticles);
  
      return { categorizedArticles };
    },
  });
  </script>
  
  <style scoped>
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  button {
    cursor: pointer;
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  
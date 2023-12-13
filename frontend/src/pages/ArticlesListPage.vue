<template>
    <div class="container mt-5">
      <h2 class="mb-4">Articles</h2>
      <div v-for="(articles, category) in categorizedArticles" :key="category" class="mb-4">
        <div class="card">
          <div class="card-header">
            <h3>{{ category }}</h3>
          </div>
          <ul class="list-group list-group-flush d-flex flex-column">
          <li v-for="article in articles" :key="article.id" class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <span>
                {{ article.title }} - by {{ article.author_name }}
                <router-link :to="`/articles/${article.id}`" class="btn btn-primary btn-sm ml-auto">View</router-link>
            </span>
            </div>
          </li>
        </ul>
      </div>
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
  
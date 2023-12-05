<template>
    <div>
      <h1>Articles</h1>
      <div v-for="category in categories" :key="category.id">
        <h2>{{ category.name }}</h2>
        <ul>
          <li v-for="article in articles[category.name]" :key="article.id">
            <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }">
              {{ article.title }}
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
  category_name: string;
}

interface Category {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const articles = reactive<Record<string, Article[]>>({});
    const categories = reactive<Category[]>([]);

    const fetchArticles = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/articles/');
        if (!response.ok) throw new Error('Failed to fetch articles');
        const data = await response.json();
        // Group articles by category
        data.forEach((article: Article) => {
          if (!articles[article.category_name]) {
            articles[article.category_name] = [];
          }
          articles[article.category_name].push(article);
        });
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const fetchCategories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/categories/');
        if (!response.ok) throw new Error('Failed to fetch categories');
        categories.push(...(await response.json()));
      } catch (error) {
        console.error('Error:', error);
      }
    };

    onMounted(() => {
      fetchArticles();
      fetchCategories();
    });

    return { articles, categories };
  },
});
</script>

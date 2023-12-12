<template>
<div class="container mt-5">
  <div v-if="article">
    <h2 class="mb-3">{{ article.title }}</h2>
    <p class="lead">{{ article.content }}</p>
    <p class="lead">Author: {{ article.author }}</p>

    <div class="mb-3">
    <h3>Comments</h3>
    <ul v-if="article.comments && article.comments.length > 0" class="list-unstyled">
      <li v-for="comment in article.comments" :key="comment.id">
        {{ comment.content }} - by {{ comment.author }}
      </li>
    </ul>
    <p v-else>No comments yet.</p>
  </div>
  </div>
  <div v-else>
    <p class="lead">Article not found or loading...</p>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
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
    const article = ref<Article | null>(null);

    const fetchArticle = async () => {
      const articleId = route.params.id;
      if (!articleId) {
        console.error('Article ID not provided');
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/articles/${articleId}/`);
        if (!response.ok) throw new Error('Failed to fetch article');
        const data = await response.json();
        article.value = data;
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
/* Add styles as needed */
</style>
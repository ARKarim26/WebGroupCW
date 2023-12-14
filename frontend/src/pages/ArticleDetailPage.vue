<template>
<div class="container mt-5">
  <div v-if="article">
    <h2 class="mb-3">{{ article.title }}</h2>
    <p>{{ article.content }}</p>
    <p>Author: {{ article.author }}</p>

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

  <!-- Add Comment Button -->
  <button @click="showModal" class="btn btn-success">Add Comment</button>

    <!-- MODAL -->
    <div class="modal fade" v-show="isModalVisible" id="commentModal" tabindex="-1" role="dialog" aria-labelledby="commentModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="commentModalLabel">Add Comment</h5>
            <button type="button" class="close" @click="hideModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <form @submit.prevent="">
              <div class="form-group">
                <label for="commentContent">Comment:</label>
                <textarea v-model="newComment.content" class="form-control" id="commentContent" rows="3" required></textarea>
              </div>
              <div class="form-group">
                <label for="commentAuthor">Your Name:</label>
                <input v-model="newComment.author" type="text" class="form-control" id="commentAuthor" required>
              </div>
              <button type="submit" class="btn btn-primary">Submit Comment</button>
            </form>
          </div>

          <!-- Add modal footer if needed -->

        </div>
      </div>
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
    const isModalVisible = ref(false);
    const newComment = ref<Comment>({
      id: 0,
      content: '',
      author: '',
    });

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

    const addComment = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/articles/${article.value?.id}/comments/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newComment.value),
        });

        if (!response.ok) {
          throw new Error('Failed to add comment');
        }
        await fetchArticle();
        hideModal();
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const showModal = () => {
      isModalVisible.value = true;
    };

    const hideModal = () => {
      isModalVisible.value = false;
    };


    onMounted(fetchArticle);
    return { article, isModalVisible, showModal, hideModal, newComment, addComment };

  }, 
});
</script>

<style scoped>
/* Add styles as needed */
</style>
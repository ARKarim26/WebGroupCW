<template>
  <div class="container mt-5">
    <div class="jumbotron">
      <h1 class="display-4">{{ title }}</h1>
      <p class="lead">Your leading source for the latest news and updates.</p>
      <hr class="my-4">
      <p>Stay informed with the most recent and relevant news from around the world.</p>

      <router-link class="btn btn-primary btn-lg" to="/articles"> Explore News </router-link>
    </div>
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";

    export default defineComponent({
        data() {
            return {
                title: "Main Page",
            }
        }
    })
</script>

<style scoped>
</style>

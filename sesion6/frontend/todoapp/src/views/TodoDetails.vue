<template>
  <div>
    <h1>{{ todo.name }}</h1>
    <div class="todo-details">
      <img :src="require(`@/assets/${todo.image}`)" :alt="todo.name" />
      <div>{{ todo.description }}</div>
    </div>
  </div>
</template>

<script>
import store from "@/store";

export default {
  data() {
    return {
      todoId: this.$route.params.id,
    };
  },
  computed: {
    todo() {
      return store.todos.find((d) => d.id === parseInt(this.todoId));
    },
  },
};
</script>

<style scoped>
img {
  max-width: 600px;
  height: auto;
  widows: auto;
}

.todo-details {
  display: flex;
  justify-content: space-between;
}
</style>

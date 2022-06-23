<template>
  <div id="nav">
    <p class="logo">The Todo App</p>
    <ul class="nav-links">
      <li class="links"><router-link to="/">Home</router-link></li>
      <li class="links" v-for="todo in todos" v-bind:key="todo.id">
        <router-link :to="{ name: 'TodoDetails', params: { id: todo.id } }">
          {{ todo.name }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import store from "@/store";

export default {
  name: "TheNavigation",
  data() {
    return {
      todos: store.todos,
    };
  },
};
</script>

<style scoped>
#nav {
  display: flex;
}

nav a {
  font-weight: bold;
  text-decoration: none;
  color: #2c3e50;
}

.nav-links {
  display: flex;
}

.links {
  padding-right: 20px;
  list-style: none;
}

.links:hover {
  text-decoration: underline;
}

.logo {
  font-size: 20px;
  color: purple;
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

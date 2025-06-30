<template>
  <main class="container">
    <h1>🩺 MedPal – Offline Medical Assistant</h1>
    <RecordButton />
  </main>
</template>

<script>
import RecordButton from './components/RecordButton.vue';

export default {
  components: {
    RecordButton
  }
};
</script>

<style scoped>
.container {
  padding-top: 10vh;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
}

button {
  padding: 0.8em 1.4em;
  font-size: 1em;
  border: none;
  border-radius: 10px;
  background-color: #1e90ff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0b6fd6;
}
</style>

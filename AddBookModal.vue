<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Add Book</h2>
      <form @submit.prevent="addBook">
        <div class="form-group">
          <label for="title">Title</label>
          <input
            type="text"
            v-model="title"
            id="title"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="author">Author</label>
          <input
            type="text"
            v-model="author"
            id="author"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            v-model="description"
            id="description"
            class="form-control"
            required
          ></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Book</button>
        <button type="button" class="btn btn-secondary" @click="$emit('close')">
          Close
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["genreId"],
  data() {
    return {
      title: "",
      author: "",
      description: "",
    };
  },
  methods: {
    addBook() {
      axios
        .post("http://127.0.0.1:5000/add-book", {
          title: this.title,
          author: this.author,
          description: this.description,
          genre_id: this.genreId,
        })
        .then(() => {
          this.$emit("refresh");
          this.$emit("close");
        })
        .catch((error) => {
          console.error("Error adding book:", error);
        });
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  max-width: 100%;
}
</style>

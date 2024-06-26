<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Add Genre</h2>
      <form @submit.prevent="addGenre">
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
          <label for="description">Description</label>
          <textarea
            v-model="description"
            id="description"
            class="form-control"
            required
          ></textarea>
        </div>
        <div class="form-group">
          <label for="image_url">Image URL</label>
          <input
            type="text"
            v-model="image_url"
            id="image_url"
            class="form-control"
          />
        </div>
        <button type="submit" class="btn btn-primary">Add Genre</button>
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
  data() {
    return {
      title: "",
      description: "",
      image_url: "",
    };
  },
  methods: {
    addGenre() {
      axios
        .post("http://127.0.0.1:5000/add-genre", {
          title: this.title,
          description: this.description,
          image_url: this.image_url,
        })
        .then(() => {
          this.$emit("refresh");
          this.$emit("close");
        })
        .catch((error) => {
          console.error("Error adding genre:", error);
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

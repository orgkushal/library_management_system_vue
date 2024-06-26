<template>
  <div class="container">
    <h1>Search Results for "{{ $route.query.query }}"</h1>
    <div v-if="books.length > 0" class="book-list">
      <div v-for="book in books" :key="book.id" class="book-container">
        <h5>{{ book.title }}</h5>
        <p>{{ book.author }}</p>
        <button
          v-if="isBookAllocated(book.id)"
          class="btn btn-secondary"
          disabled
        >
          Already Allocated
        </button>
        <button v-else @click="requestBook(book.id)" class="btn btn-primary">
          Request Book
        </button>
        <button @click="viewFeedback(book.id)" class="btn btn-info">
          View Feedback
        </button>
      </div>
    </div>
    <div v-else>
      <p>No books found for the search query.</p>
    </div>
    <button @click="goBack" class="btn btn-secondary">Back</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      books: [],
      requests_all: [],
    };
  },
  mounted() {
    this.searchBooks();
    this.fetchRequests();
  },
  methods: {
    searchBooks() {
      const query = this.$route.query.query;
      axios
        .get("http://127.0.0.1:5000/search", {
          params: { query },
        })
        .then((response) => {
          this.books = response.data.books;
        })
        .catch((error) => {
          console.error("Error searching books:", error);
        });
    },
    fetchRequests() {
      axios
        .get("http://127.0.0.1:5000/requests-for-all-books")
        .then((response) => {
          this.requests_all = response.data.requests;
        })
        .catch((error) => {
          console.error("Error fetching requests:", error);
        });
    },
    isBookAllocated(bookId) {
      return this.requests_all.some((request) => request.book_id === bookId);
    },
    requestBook(bookId) {
      const userId = sessionStorage.getItem("userId");
      axios
        .post("http://127.0.0.1:5000/request-book", {
          user_id: userId,
          book_id: bookId,
        })
        .then(() => {
          alert("Book request sent successfully!");
          this.fetchRequests();
        })
        .catch((error) => {
          console.error("Error requesting book:", error);
        });
    },
    viewFeedback(bookId) {
      this.$router.push({ name: "BookDetails", params: { id: bookId } });
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.book-list {
  margin-top: 20px;
}

.book-container {
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.btn {
  margin-right: 10px;
}
</style>

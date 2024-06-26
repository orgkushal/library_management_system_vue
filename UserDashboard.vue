<template>
  <div class="container">
    <h1>Welcome to your Dashboard</h1>

    <!-- Logout button and Search bar -->
    <div class="top-bar">
      <button class="logout-button" @click="logout">Logout</button>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          placeholder="Search books or authors..."
          class="search-input"
        />
        <button @click="performSearch" class="search-button">Search</button>
      </div>
    </div>

    <!-- Tabs for All Books and My Books -->
    <div class="tabs">
      <button
        :class="{ active: currentTab === 'all' }"
        @click="currentTab = 'all'"
      >
        All Books
      </button>
      <button
        :class="{ active: currentTab === 'my' }"
        @click="currentTab = 'my'"
      >
        My Books
      </button>
    </div>

    <div v-if="currentTab === 'all'">
      <!-- Display genres -->
      <div class="genre-list">
        <div v-for="genre in genres" :key="genre.id" class="genre-container">
          <h4>{{ genre.title }}</h4>
          <p>{{ genre.description }}</p>
          <img
            v-if="genre.image_url"
            :src="genre.image_url"
            alt="Genre Image"
            class="genre-image"
          />
          <p class="date-created">
            Created on: {{ new Date(genre.date_created).toLocaleDateString() }}
          </p>

          <!-- Display books in the genre -->
          <div class="book-list">
            <div
              v-for="book in genre.books"
              :key="book.id"
              class="book-container"
            >
              <h5>{{ book.title }}</h5>
              <p>{{ book.author }}</p>
              <p class="date-created">
                Added on: {{ new Date(book.date_created).toLocaleDateString() }}
              </p>
              <button
                v-if="isBookAllocated(book.id)"
                class="btn btn-secondary"
                disabled
              >
                Already Allocated
              </button>
              <button
                v-else
                class="btn btn-primary"
                @click="requestBook(book.id)"
              >
                Request Book
              </button>
              <button @click="viewFeedback(book.id)" class="btn btn-info">
                View Feedback
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="currentTab === 'my'">
      <h2>My Books</h2>
      <div v-if="myBooks.length > 0" class="book-list">
        <div v-for="book in myBooks" :key="book.id" class="book-container">
          <h5>{{ book.title }}</h5>
          <p>{{ book.author }}</p>
          <button @click="returnBook(book.id)" class="btn btn-danger">
            Return Book
          </button>
          <button @click="readBook(book.id)" class="btn btn-info">Read</button>
          <button @click="viewFeedback(book.id)" class="btn btn-info">
            View Feedback
          </button>
        </div>
      </div>
      <div v-else>
        <p>No books requested yet.</p>
      </div>
    </div>

    <!-- Feedback Modal -->
    <div v-if="showFeedbackModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeFeedbackModal">&times;</span>
        <h2>Feedback for {{ selectedBook.title }}</h2>
        <div v-if="feedbacks.length">
          <div v-for="item in feedbacks" :key="item.id" class="feedback-item">
            <p>{{ item.feedback_text }}</p>
            <small>{{ new Date(item.date_created).toLocaleString() }}</small>
          </div>
        </div>
        <div v-else>
          <p>No feedback available for this book.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      genres: [],
      myBooks: [],
      currentTab: "all",
      userId: null,
      requests_all: [],
      feedbacks: [],
      selectedBook: {},
      showFeedbackModal: false,
      searchQuery: "",
      // searchResults: [],
    };
  },
  mounted() {
    this.userId = sessionStorage.getItem("userId"); // Assuming user ID is stored in local storage
    this.fetchGenres();
    this.fetchMyBooks();
    this.fetchRequests();
  },
  methods: {
    fetchGenres() {
      axios
        .get("http://127.0.0.1:5000/genres")
        .then((response) => {
          this.genres = response.data.genres.map((genre) => ({
            ...genre,
            books: [],
          }));
          this.genres.forEach((genre) => {
            this.fetchBooks(genre.id);
          });
        })
        .catch((error) => {
          console.error("Error fetching genres:", error);
        });
    },
    fetchBooks(genreId) {
      axios
        .get(`http://127.0.0.1:5000/genres/${genreId}/books`)
        .then((response) => {
          const genre = this.genres.find((g) => g.id === genreId);
          genre.books = response.data.books;
        })
        .catch((error) => {
          console.error(`Error fetching books for genre ${genreId}:`, error);
        });
    },
    requestBook(bookId) {
      if (this.myBooks.length >= 5) {
        alert("Maximum book limit reached!");
        return;
      }
      axios
        .post("http://127.0.0.1:5000/request-book", {
          user_id: this.userId,
          book_id: bookId,
        })
        .then(() => {
          alert("Book request sent successfully!");
        })
        .catch((error) => {
          console.error("Error requesting book:", error);
        });
    },
    fetchMyBooks() {
      axios
        .get(`http://127.0.0.1:5000/users/${this.userId}/books`)
        .then((response) => {
          this.myBooks = response.data.books;
        })
        .catch((error) => {
          console.error("Error fetching my books:", error);
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
    returnBook(bookId) {
      const userId = this.userId; // Assume this method gets the current user's ID
      axios
        .post(`http://127.0.0.1:5000/return-book/${bookId}`, {
          user_id: userId,
        })
        .then(() => {
          this.fetchRequests();
          this.fetchMyBooks();
        })
        .catch((error) => {
          console.error("Error returning book:", error);
        });
    },
    readBook(bookId) {
      this.$router.push({ name: "BookDetails", params: { id: bookId } });
    },
    viewFeedback(bookId) {
      axios
        .get(`http://127.0.0.1:5000/feedback/${bookId}`)
        .then((response) => {
          this.feedbacks = response.data.feedbacks;
          this.selectedBook = this.genres
            .flatMap((genre) => genre.books)
            .find((book) => book.id === bookId);
          this.showFeedbackModal = true;
        })
        .catch((error) => {
          console.error("Error fetching feedback:", error);
        });
    },
    closeFeedbackModal() {
      this.showFeedbackModal = false;
      this.feedback = [];
    },
    performSearch() {
      this.$router.push({
        name: "SearchResults",
        query: { query: this.searchQuery },
      });
    },
    logout() {
      this.$router.push("/login"); // Redirect to login page
      this.genres = []; // Reset genres data
      console.log("Logging out...");
    },
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
.container {
  padding: 20px;
  position: relative;
}

.logout-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
}

.search-bar {
  display: flex;
  align-items: center;
}

.search-input {
  padding: 10px;
  font-size: 16px;
  border-radius: 5px 0 0 5px;
  border: 1px solid #ccc;
  border-right: none;
  outline: none;
}

.search-button {
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 0 5px 5px 0;
  border: 1px solid #ccc;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  outline: none;
  border-left: none;
}

.search-button:hover {
  background-color: #0056b3;
}
.tabs {
  display: flex;
  margin-bottom: 20px;
}

.tabs button {
  flex: 1;
  padding: 10px;
  cursor: pointer;
  background-color: #f1f1f1;
  border: none;
  font-size: 16px;
}

.tabs button.active {
  background-color: #007bff;
  color: white;
}

.genre-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.genre-container {
  width: calc(33.333% - 20px);
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.genre-image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
  margin-top: 10px;
}

.date-created {
  font-size: 0.8em;
  color: #777;
}

.book-list {
  margin-top: 10px;
  width: 100%;
}

.book-container {
  background-color: #fff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.feedback-item {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}

.feedback-item:last-child {
  border-bottom: none;
}
</style>

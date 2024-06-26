<template>
  <div class="container">
    <h1>Welcome Admin</h1>
    <!-- Logout Button -->
    <button class="logout-button" @click="logout">Logout</button>

    <!-- Tabs -->
    <div class="tabs">
      <button
        @click="currentTab = 'genres'"
        :class="{ active: currentTab === 'genres' }"
      >
        Genres
      </button>
      <button
        @click="currentTab = 'requests'"
        :class="{ active: currentTab === 'requests' }"
      >
        Requests
      </button>
    </div>

    <!-- Genres Tab -->
    <div v-if="currentTab === 'genres'">
      <!-- Existing code for genres and books management -->
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

          <div class="options-row">
            <div>
              <button @click="editGenre(genre)" class="btn btn-warning">
                Edit
              </button>
              <button @click="deleteGenre(genre.id)" class="btn btn-danger">
                Delete
              </button>
            </div>
            <div>
              <button
                @click="showAddBookModal(genre.id)"
                class="btn btn-primary"
              >
                Add Book
              </button>
              <button @click="fetchBooks(genre.id)" class="btn btn-info">
                Display Books
              </button>
            </div>
          </div>

          <div v-if="genre.showBooks" class="book-list">
            <div
              v-for="book in genre.books"
              :key="book.id"
              class="book-container"
            >
              <h5>{{ book.title }}</h5>
              <p>{{ book.author }}</p>
              <!-- <p>{{ book.description }}</p> -->
              <p class="date-created">
                Added on: {{ new Date(book.date_created).toLocaleDateString() }}
              </p>
              <p v-if="allocatedBooks[book.id]">
                <strong>Allocated to:</strong>
                {{ allocatedBooks[book.id].user_email }}
                <strong>On:</strong>
                {{ allocatedBooks[book.id].issue_date }}
                <button @click="returnBook(book.id)" class="btn btn-danger">
                  End Access
                </button>
              </p>
              <div>
                <button @click="editBook(book)" class="btn btn-warning">
                  Edit
                </button>
                <button @click="deleteBook(book.id)" class="btn btn-danger">
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal" v-if="showModal">
        <div class="modal-content">
          <span class="close" @click="closeModal">&times;</span>
          <h2>{{ isEditing ? "Edit Genre" : "Add New Genre" }}</h2>
          <form @submit.prevent="submitGenre">
            <div class="form-group">
              <label for="title">Title</label>
              <input
                type="text"
                class="form-control"
                id="title"
                v-model="newGenre.title"
                required
              />
            </div>
            <div class="form-group">
              <label for="description">Description</label>
              <textarea
                class="form-control"
                id="description"
                v-model="newGenre.description"
                required
              ></textarea>
            </div>
            <div class="form-group">
              <label for="image_url">Image URL (Optional)</label>
              <input
                type="text"
                class="form-control"
                id="image_url"
                v-model="newGenre.image_url"
              />
            </div>
            <button type="submit" class="btn btn-primary">
              {{ isEditing ? "Update Genre" : "Add Genre" }}
            </button>
          </form>
        </div>
      </div>

      <div class="modal" v-if="showBookModal">
        <div class="modal-content">
          <span class="close" @click="closeBookModal">&times;</span>
          <h2>{{ isEditingBook ? "Edit Book" : "Add New Book" }}</h2>
          <form @submit.prevent="submitBook">
            <div class="form-group">
              <label for="bookTitle">Title</label>
              <input
                type="text"
                class="form-control"
                id="bookTitle"
                v-model="newBook.title"
                required
              />
            </div>
            <div class="form-group">
              <label for="author">Author</label>
              <input
                type="text"
                class="form-control"
                id="author"
                v-model="newBook.author"
                required
              />
            </div>
            <div class="form-group">
              <label for="description">Content</label>
              <textarea
                class="form-control"
                id="description"
                v-model="newBook.description"
              ></textarea>
            </div>
            <button type="submit" class="btn btn-primary">
              {{ isEditingBook ? "Update Book" : "Add Book" }}
            </button>
          </form>
        </div>
      </div>

      <button class="add-genre-button" @click="showAddGenreModal">+</button>
    </div>

    <div v-if="currentTab === 'requests'">
      <h2>User Requests</h2>
      <div
        v-for="request in requests"
        :key="request.id"
        class="request-container"
      >
        <p><strong>User:</strong> {{ request.user_name }}</p>
        <p><strong>Book:</strong> {{ request.book_title }}</p>
        <p><strong>Status:</strong> {{ request.status }}</p>
        <button @click="acceptRequest(request.id)" class="btn btn-success">
          Accept
        </button>
        <button @click="rejectRequest(request.id)" class="btn btn-danger">
          Reject
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentTab: "genres",
      showModal: false,
      showBookModal: false,
      isEditing: false,
      isEditingBook: false,
      newGenre: {
        title: "",
        description: "",
        image_url: "",
      },
      newBook: {
        title: "",
        author: "",
        description: "",
      },
      genres: [],
      requests: [],
      currentGenreId: null,
      currentBookId: null,
      currentBookGenreId: null,
      allocatedBooks: {},
    };
  },
  mounted() {
    this.fetchGenres();
    this.fetchRequests();
  },
  methods: {
    showAddGenreModal() {
      this.isEditing = false;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    showAddBookModal(genreId) {
      this.isEditingBook = false;
      this.currentBookGenreId = genreId;
      this.showBookModal = true;
    },
    closeBookModal() {
      this.showBookModal = false;
      this.resetBookForm();
    },
    resetForm() {
      this.newGenre.title = "";
      this.newGenre.description = "";
      this.newGenre.image_url = "";
      this.currentGenreId = null;
    },
    resetBookForm() {
      this.newBook.title = "";
      this.newBook.author = "";
      this.newBook.description = "";
      this.currentBookId = null;
      this.currentBookGenreId = null;
    },
    submitGenre() {
      if (this.isEditing) {
        this.updateGenre();
      } else {
        this.addGenre();
      }
    },
    submitBook() {
      if (this.isEditingBook) {
        this.updateBook();
      } else {
        this.addBook();
      }
    },
    addGenre() {
      axios
        .post("http://127.0.0.1:5000/add-genre", this.newGenre)
        .then((response) => {
          this.genres.push(response.data.genre);
          this.closeModal();
        })
        .catch((error) => {
          console.error("Error adding genre:", error);
        });
    },
    addBook() {
      axios
        .post("http://127.0.0.1:5000/add-book", {
          ...this.newBook,
          genre_id: this.currentBookGenreId,
        })
        .then((response) => {
          const genre = this.genres.find(
            (g) => g.id === this.currentBookGenreId
          );
          if (!genre.books) genre.books = [];
          genre.books.push(response.data.book);
          this.closeBookModal();
        })
        .catch((error) => {
          console.error("Error adding book:", error);
        });
    },
    editGenre(genre) {
      this.newGenre = { ...genre };
      this.currentGenreId = genre.id;
      this.isEditing = true;
      this.showModal = true;
    },
    updateGenre() {
      axios
        .put(
          `http://127.0.0.1:5000/edit-genre/${this.currentGenreId}`,
          this.newGenre
        )
        .then((response) => {
          const index = this.genres.findIndex(
            (g) => g.id === this.currentGenreId
          );
          this.genres.splice(index, 1, response.data.genre);
          this.closeModal();
        })
        .catch((error) => {
          console.error("Error updating genre:", error);
        });
    },
    deleteGenre(genreId) {
      axios
        .delete(`http://127.0.0.1:5000/delete-genre/${genreId}`)
        .then(() => {
          this.genres = this.genres.filter((g) => g.id !== genreId);
        })
        .catch((error) => {
          console.error("Error deleting genre:", error);
        });
    },
    editBook(book) {
      this.newBook = { ...book };
      this.currentBookId = book.id;
      this.currentBookGenreId = book.genre_id;
      this.isEditingBook = true;
      this.showBookModal = true;
    },
    updateBook() {
      axios
        .put(
          `http://127.0.0.1:5000/edit-book/${this.currentBookId}`,
          this.newBook
        )
        .then((response) => {
          const genre = this.genres.find(
            (g) => g.id === this.currentBookGenreId
          );
          const index = genre.books.findIndex(
            (b) => b.id === this.currentBookId
          );
          genre.books.splice(index, 1, response.data.book);
          this.closeBookModal();
        })
        .catch((error) => {
          console.error("Error updating book:", error);
        });
    },
    deleteBook(bookId) {
      axios
        .delete(`http://127.0.0.1:5000/delete-book/${bookId}`)
        .then(() => {
          const genre = this.genres.find((g) =>
            g.books.find((b) => b.id === bookId)
          );
          genre.books = genre.books.filter((b) => b.id !== bookId);
        })
        .catch((error) => {
          console.error("Error deleting book:", error);
        });
    },
    returnBook(bookId) {
      const userId = this.userId; // Assume this method gets the current user's ID
      axios
        .post(`http://127.0.0.1:5000/return-book/${bookId}`, {
          user_id: userId,
        })
        .then(() => {
          this.fetchRequests();
          this.fetchAllocatedBooks();
        })
        .catch((error) => {
          console.error("Error returning book:", error);
        });
    },
    fetchGenres() {
      axios
        .get("http://127.0.0.1:5000/genres")
        .then((response) => {
          this.genres = response.data.genres.map((genre) => ({
            ...genre,
            showBooks: false,
            books: [],
          }));
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
          genre.showBooks = !genre.showBooks;
          this.fetchAllocatedBooks();
        })
        .catch((error) => {
          console.error(`Error fetching books for genre ${genreId}:`, error);
        });
    },
    fetchAllocatedBooks() {
      axios
        .get("http://127.0.0.1:5000/requests/all")
        .then((response) => {
          this.allocatedBooks = response.data.requests.reduce((acc, req) => {
            acc[req.book_id] = req;
            return acc;
          }, {});
        })
        .catch((error) => {
          console.error("Error fetching allocated books:", error);
        });
    },
    fetchRequests() {
      axios
        .get("http://127.0.0.1:5000/requests")
        .then((response) => {
          this.requests = response.data.requests;
        })
        .catch((error) => {
          console.error("Error fetching requests:", error);
        });
    },
    acceptRequest(requestId) {
      axios
        .post(`http://127.0.0.1:5000/requests/${requestId}/accept`)
        .then(() => {
          this.fetchRequests();
        })
        .catch((error) => {
          console.error("Error accepting request:", error);
        });
    },
    rejectRequest(requestId) {
      axios
        .post(`http://127.0.0.1:5000/requests/${requestId}/reject`)
        .then(() => {
          this.fetchRequests();
        })
        .catch((error) => {
          console.error("Error rejecting request:", error);
        });
    },
    logout() {
      this.$router.push("/login");
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
}

.tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background-color: #f1f1f1;
  cursor: pointer;
}

.tabs button.active {
  background-color: #007bff;
  color: #fff;
}

.request-container {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.btn {
  margin: 5px;
}

.logout-button {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-genre-button {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #007bff;
  color: #fff;
  font-size: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
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
</style>

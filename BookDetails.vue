<template>
  <body>
    <div class="container">
      <h1>{{ book.title }}</h1>
      <p><strong>Author:</strong> {{ book.author }}</p>
      <p>{{ book.description }}</p>
      <button @click="goBack" class="btn btn-secondary">Back</button>
      <button @click="showFeedbackForm" class="btn btn-primary">
        Give Feedback
      </button>

      <!-- Feedback Modal -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeModal">&times;</span>
          <h2>Give Feedback for {{ book.title }}</h2>
          <form @submit.prevent="submitFeedback">
            <div class="form-group">
              <label for="feedback">Feedback</label>
              <textarea
                id="feedback"
                v-model="feedbackText"
                class="form-control"
                required
              ></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      book: {},
      showModal: false,
      feedbackText: "",
    };
  },
  created() {
    this.fetchBookDetails();
  },
  methods: {
    fetchBookDetails() {
      const bookId = this.$route.params.id; // Get the ID from route parameters
      axios
        .get(`http://127.0.0.1:5000/book/${bookId}`)
        .then((response) => {
          this.book = response.data;
        })
        .catch((error) => {
          console.error("Error fetching book details:", error);
        });
    },
    goBack() {
      this.$router.go(-1);
    },
    showFeedbackForm() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.feedbackText = "";
    },
    submitFeedback() {
      const userId = sessionStorage.getItem("userId");
      const bookId = this.$route.params.id;
      axios
        .post(`http://127.0.0.1:5000/feedback`, {
          user_id: userId,
          book_id: bookId,
          feedback_text: this.feedbackText,
        })
        .then(() => {
          alert("Feedback submitted successfully!");
          this.closeModal();
        })
        .catch((error) => {
          console.error("Error submitting feedback:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Container styles */
.container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.3); /* Semi-transparent background */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Soft shadow */
  border-radius: 8px; /* Rounded corners */
  text-align: center; /* Centered text */
  font-family: "Arial", sans-serif; /* Font family */
}

/* Header styles */
h1 {
  font-size: 2.5em; /* Large font size */
  color: #000000; /* Dark text color */
  margin-bottom: 20px; /* Space below the header */
}

/* Paragraph styles */
p {
  font-size: 1.2em; /* Medium font size */
  color: #e6e4e4; /* Medium-dark text color */
  line-height: 1.6; /* Line height for readability */
  margin-bottom: 20px; /* Space below paragraphs */
}

/* Strong tag styles */
strong {
  color: #000; /* Bold text color */
}

/* Button styles */
.btn {
  padding: 10px 20px; /* Padding around the button */
  font-size: 1em; /* Button font size */
  border: none; /* No border */
  border-radius: 5px; /* Rounded corners */
  cursor: pointer; /* Pointer cursor on hover */
  transition: background 0.3s; /* Smooth background color transition */
}

/* Secondary button styles */
.btn-secondary {
  background: #007bff; /* Blue background */
  color: white; /* White text */
}

.btn-secondary:hover {
  background: #0056b3; /* Darker blue on hover */
}

/* Primary button styles */
.btn-primary {
  background: #28a745; /* Green background */
  color: white; /* White text */
}

.btn-primary:hover {
  background: #218838; /* Darker green on hover */
}

/* Modal styles */
.modal {
  display: block; /* Show the modal */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
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

/* Background image for the body */
body {
  background-image: url("/public/images/pexels-pixabay-235985.jpg");
  background-size: cover; /* Cover the whole page */
}
</style>

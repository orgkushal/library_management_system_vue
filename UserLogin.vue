<template>
  <body>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h3 class="card-title text-center mb-4">Login</h3>
              <form @submit.prevent="login">
                <div class="form-group mb-3">
                  <label for="email">Email</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="email"
                  />
                </div>
                <div class="form-group mb-3">
                  <label for="password">Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    v-model="password"
                  />
                </div>
                <button type="submit" class="btn btn-primary btn-block">
                  Login
                </button>
                <button
                  type="button"
                  class="btn btn-secondary btn-block mt-2"
                  @click="goToRegister"
                >
                  Register
                </button>
                <div v-if="message" :class="messageClass" class="mt-3">
                  {{ message }}
                </div>
              </form>
            </div>
          </div>
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
      email: "",
      password: "",
      message: "",
      messageClass: "",
    };
  },
  methods: {
    login() {
      axios
        .post("http://127.0.0.1:5000/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          const userId = response.data.userId; // Assuming this is how you get the user ID from the response
          sessionStorage.setItem("userId", userId); // Store user ID in session storage
          this.message = response.data.message;
          this.messageClass = "alert alert-success";
          if (response.data.role === "librarian") {
            this.$router.push("/librarian-dashboard");
          } else {
            this.$router.push("/user-dashboard");
          }
        })
        .catch((error) => {
          this.message = error.response.data.error;
          this.messageClass = "alert alert-danger";
        });
    },
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
body,
html {
  background-image: url("/public/images/pexels-engin-akyurt-2946974.jpg"); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  padding: 5cm;
  box-sizing: border-box;
  padding: 0;
  height: 100%;
}

.container {
  padding: 5cm;
  box-sizing: border-box;
}

.card {
  width: 100%;
  max-width: 400px; /* Adjust maximum width of the form */
  background: #fff; /* Background color for the form */
  padding: 20px; /* Padding inside the card */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Box shadow for the card */
}

.btn-block {
  width: 100%; /* Make button stretch to fill container */
}
</style>

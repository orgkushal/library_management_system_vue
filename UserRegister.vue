<template>
  <body>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h3 class="card-title text-center mb-4">Register</h3>
              <form @submit.prevent="register">
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
                <div class="form-group mb-3">
                  <label for="confirmPassword">Confirm Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="confirmPassword"
                    v-model="confirmPassword"
                  />
                </div>
                <button type="submit" class="btn btn-primary btn-block">
                  Register
                </button>
                <button
                  type="button"
                  class="btn btn-secondary btn-block mt-2"
                  @click="goToLogin"
                >
                  Login
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
      confirmPassword: "",
      message: "",
      messageClass: "",
    };
  },
  methods: {
    register() {
      if (this.password !== this.confirmPassword) {
        this.message = "Passwords do not match.";
        this.messageClass = "alert alert-danger";
        return;
      }

      axios
        .post("http://127.0.0.1:5000/register", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          this.message = response.data.message;
          this.messageClass = "alert alert-success";
        })
        .catch((error) => {
          this.message = error.response.data.error;
          this.messageClass = "alert alert-danger";
        });
    },
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
body,
html {
  background-image: url("/public/images/pexels-engin-akyurt-2952871.jpg"); /* Adjust the path to your image */
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

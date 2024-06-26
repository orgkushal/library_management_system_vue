import { createRouter, createWebHistory } from "vue-router";
import UserLogin from "../components/UserLogin.vue";
import UserRegister from "../components/UserRegister.vue";
import UserDashboard from "../components/UserDashboard.vue";
import LibrarianDashboard from "../components/LibrarianDashboard.vue";
import BookDetails from "../components/BookDetails.vue";
import SearchResults from "../components/SearchResults.vue";

const routes = [
  { path: "/login", component: UserLogin },
  { path: "/register", component: UserRegister },
  { path: "/user-dashboard", component: UserDashboard },
  { path: "/librarian-dashboard", component: LibrarianDashboard },
  { path: "/", redirect: "/login" },
  {
    path: "/book/:id",
    name: "BookDetails",
    component: BookDetails,
  },
  {
    path: "/search",
    name: "SearchResults",
    component: SearchResults,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

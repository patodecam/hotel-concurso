<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-primary text-white text-center">
            <h2>Admin Login</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="form-group mb-3">
                <label for="username">Username</label>
                <input 
                  type="text" 
                  v-model="username" 
                  id="username" 
                  class="form-control" 
                  placeholder="Enter username" 
                  required 
                />
              </div>
              <div class="form-group mb-3">
                <label for="password">Password</label>
                <input 
                  type="password" 
                  v-model="password" 
                  id="password" 
                  class="form-control" 
                  placeholder="Enter password" 
                  required 
                />
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
              <p v-if="errorMessage" class="text-danger mt-3 text-center">{{ errorMessage }}</p>
            </form>
          </div>
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
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    login() {
      // Enviamos la solicitud POST al backend para obtener el token
      axios
        .post("http://localhost:8000/api/login/", {
          username: this.username,
          password: this.password, 
        })
        .then((response) => {
          // Si la respuesta es exitosa, guardamos los tokens y el estado del admin
          localStorage.setItem("token", response.data.access);
          localStorage.setItem("refresh", response.data.refresh);
          localStorage.setItem("isAdmin", response.data.is_staff ? "true" : "false");

          // Redirigimos al usuario a la página de lista de usuarios (o dashboard)
          this.$router.push("/admin/users");
        })
        .catch((error) => {
          // Manejo de errores si las credenciales son incorrectas o algún otro problema
          if (error.response && error.response.status === 401) {
            this.errorMessage = "Credenciales incorrectas. Intenta de nuevo.";
          } else {
            this.errorMessage = "Hubo un problema con la autenticación. Intenta más tarde.";
          }
        });
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>

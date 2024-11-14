
<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Lista de Participantes</h2>
    <div class="table-responsive">
      <table class="table table-striped table-bordered">
        <thead class="thead-dark">
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Name</th>
            <th>Rut</th>
            <th>Email</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.first_name + ' ' + user.last_name }}</td>
            <td>{{ user.rut + '-' + user.dv }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.direccion }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="errorMessage" class="text-danger text-center mt-3">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      errorMessage: "",
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      const token = localStorage.getItem("token");
      axios
        .get("http://localhost:8000/api/users/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          if (error.response && error.response.status === 403) {
            this.errorMessage = "No tienes permiso para ver esta información.";
          } else {
            this.errorMessage =
              "Hubo un problema al cargar la lista de usuarios.";
          }
        });
    },
  },
};
</script>

<style scoped>
h2 {
  font-size: 1.8rem;
  font-weight: bold;
}
.table {
  margin-top: 20px;
}
.text-danger {
  color: red;
}
</style>
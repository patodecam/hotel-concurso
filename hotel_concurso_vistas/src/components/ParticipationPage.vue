<template>
    <div class="container mt-5">
      <h2>Participar en el Sorteo</h2>
      <p class="text-muted">Completa el siguiente formulario para participar en el sorteo. Asegúrate de que toda la información sea correcta.</p>
      <button class="btn btn-primary" @click="mostrarFormulario">Participar</button>
      
      <div v-if="formularioVisible" class="mt-4">
        <form @submit.prevent="enviarParticipacion" class="form-group">
          <div>
            <label for="username">Nombre de Usuario:</label>
            <input type="text" v-model="username" required class="form-control" />
          </div>
          <div>
            <label for="first_name">Nombre:</label>
            <input type="text" v-model="first_name" required class="form-control" />
          </div>
          <div>
            <label for="last_name">Apellido:</label>
            <input type="text" v-model="last_name" required class="form-control" />
          </div>
          <div>
            <label for="email">Correo:</label>
            <input type="email" v-model="email" required class="form-control" />
          </div>
          <div>
            <label for="rut">RUT:</label>
            <input type="text" v-model="rut" required class="form-control" />
          </div>
          <div>
            <label for="dv">DV:</label>
            <input type="text" v-model="dv" required maxlength="1" class="form-control" />
          </div>
          <div>
            <label for="direccion">Dirección:</label>
            <input type="text" v-model="direccion" required class="form-control" />
          </div>
          <button type="submit" class="btn btn-success mt-3">Enviar</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ParticipacionSorteo',
    data() {
      return {
        formularioVisible: false,
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        rut: '',
        dv: '',
        region: '',
        ciudad: '',
        direccion: '',
      };
    },
    methods: {
      mostrarFormulario() {
        this.formularioVisible = true;
      },
      async enviarParticipacion() {
        const datosUsuario = {
          username: this.username,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          rut: this.rut,
          dv: this.dv,
          region: this.region,
          ciudad: this.ciudad,
          direccion: this.direccion,
        };
  
        try {
          const response = await fetch('http://localhost:8000/api/registro/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(datosUsuario),
          });
  
          if (!response.ok) {
            alert('Error al enviar la participación.');
          } else {
            alert('Participación enviada con éxito.');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  </style>
  
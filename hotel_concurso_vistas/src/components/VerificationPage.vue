<template>
    <div class="container mt-5">
        <h1 class="text-center">Verificación de Correo Electrónico</h1>
        <form @submit.prevent="verifyEmail" class="mt-4">
            <div class="form-group">
                <label for="password">Nueva Contraseña</label>
                <input type="password" id="password" v-model="password" class="form-control" required />
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirmar Contraseña</label>
                <input type="password" id="confirm_password" v-model="confirmPassword" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary btn-block">Verificar y Establecer Contraseña</button>
            <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
            <p v-if="successMessage" class="text-success mt-2">{{ successMessage }}</p>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            password: '',
            confirmPassword: '',
            errorMessage: null,
            successMessage: null,
        };
    },

    methods: {
        verifyEmail() {
            if (this.password !== this.confirmPassword) {
                this.errorMessage = "Las contraseñas no coinciden.";
                this.successMessage = null;
                return;
            }

            const { uidb64, token } = this.$route.params;
            axios.post(`http://localhost:8000/api/verify/${uidb64}/${token}/`, {
                password: this.password 
            })
            .then(response => {
                this.successMessage = response.data.message;
                this.errorMessage = null;
                // Redirigir a la página principal después de un éxito
                this.$router.push({ name: 'home' });
            })
            .catch(error => {
                this.errorMessage = error.response?.data?.error || "Error al verificar el correo.";
                this.successMessage = null;
            });
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}
</style>

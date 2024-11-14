<template>
    <div>
      <div class="contest-announcement">
        <h2>¡Participa en nuestro Concurso de Viaje!</h2>
        <p>¡Tienes la oportunidad de ganar un increíble viaje! Inscríbete ahora y no te pierdas esta oportunidad única.</p>
        <router-link to="/participation">
          <button class="participate-button">¡Participa Ahora!</button>
        </router-link>
  
        
        <div class="login-prompt">
          <p>¿Ya tienes una cuenta? Inicia sesión:
            (Solo para credenciales de administrador)
          </p>
          <router-link to="/login">
            <button class="login-button">Iniciar Sesión</button>
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .participate-button,
  .login-button {
    margin-top: 10px;
    padding: 10px 15px;
    background-color: #42b983; 
    color: white; 
    border: none; 
    border-radius: 5px; 
    cursor: pointer; 
  }
  
  .participate-button:hover,
  .login-button:hover {
    background-color: #36a074; 
  }
  
  .login-prompt {
    margin-top: 20px; 
  }
  </style>
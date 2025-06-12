<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      message: 'Cargando...'
    }
  },
  mounted() {
    this.$axios.get('http://localhost:5000/api/data')
      .then(response => {
        this.message = response.data.message
      })
      .catch(error => {
        console.error('Error al obtener datos:', error)
      })
  }
}
</script>

<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-primary">
 <a class="navbar-brand d-flex align-items-center" href="#">
    <i class="bi bi-shop me-2"></i> <!-- ícono con margen a la derecha -->
    SuperMarket
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
  <li class="nav-item active">
    <router-link to="/registro" class="nav-link d-flex align-items-center">
     <i class="bi bi-person-add me-2"></i>
      Registrarse</router-link>  
  </li>
  <li class="nav-item active">
    <router-link to="/login" class="nav-link d-flex align-items-center">
     <i class="bi bi-person me-2"></i>
     Iniciar sesión</router-link>
  </li>
  <li class="nav-item me-3">
    <router-link to="/login_admin"  class="nav-link d-flex align-items-center">
     <i class="bi bi-person-gear me-2"></i>Login Admin</router-link>
  </li>
</ul>

  </div>
</nav>
 
  <h2>Bienvenido a la página de venta de productos online!</h2>
  <div class="hello">
    <h3>{{ message }}</h3>
   </div>

</template>

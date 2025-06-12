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
        <router-link to="/realizar_pedido" class="nav-link d-flex align-items-center">
        <i class="bi bi-shop-window me-2"></i>
        Realizar un pedido
      </router-link>
      </li>
      <li class="nav-item active">
            <router-link to="/ver_pedidos" class="nav-link d-flex align-items-center">
              <i class="bi bi-cart me-2"></i>
              Ver mis pedidos</router-link>
      </li>
      <li class="nav-item active">
            <router-link to="/cerrar_sesion" class="nav-link d-flex align-items-center">
            <i class="bi bi-box-arrow-right me-2"></i>    
            Cerrar sesión
            </router-link>
      </li>

    </ul>
  </div>
</nav>
 
    <h1>Página de Inicio</h1>
    <div class="mx-auto mt-3 p-5" style="width: 400px;" >
      <p v-if="message" v-html="message" :class="messageClass"></p>
    </div>
 
  <p v-if="mensaje_ext" class="alert alert-info">{{ mensaje_ext }}</p>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Inicio',
  data() {
    return {
      message: 'Cargando...',
      mensaje_ext: this.$route.query.mensaje_ext || ''
    }
  },
  async mounted() { 
     if (this.mensaje_ext) {
      setTimeout(() => {
        this.mensaje_ext = '';
      }, 4000); // Opcional: oculta mensaje luego de 4 segundos
    }
    try {
      const response = await axios.get('http://localhost:5000/api/inicio', { withCredentials: true });
      this.message = response.data.message;
    } catch (error) {
      if (error.response && error.response.status === 401) {
        
      } else {
        this.message = 'Error al obtener los datos.';
      }
    }
  },
   
  
}

</script>

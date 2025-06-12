<template>
    <div>
        <h2 class="text-center display-5">¿Seguro que quieres cerrar sesión?</h2>
        <div class="pt-5 d-flex justify-content-center gap-3">
            <button @click="cerrarSesion" class="btn btn-danger">Cerrar sesión</button>
            <button @click="Volver" class="btn btn-primary">Volver al inicio</button>
        </div>
    </div>
    <div class='mt-3'>
        <p v-if="message" :class="messageClass">{{ message }}</p>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name: 'LogoutAdmin',
    data(){
        return{
            message:'',
            messageClass: '',

        }
    },
    methods:{
        async cerrarSesion()
        {
            try {
                const respuesta = await axios.post('http://localhost:5000/api/logout_admin', {}, { withCredentials: true });
                this.message = respuesta.data.message
                this.$router.push('/');  // Asegúrate de que /home esté definido en el router


    } catch (error) {
      console.error('Error Al cerrar sesión:', error);
      this.messageClass = 'text-danger'
      this.message = 'Error al cerrar sesión! [Error del servidor]'}
  },
  Volver()
{
    this.$router.push('/inicio');  // Asegúrate de que /home esté definido en el router

}
},

}
</script>
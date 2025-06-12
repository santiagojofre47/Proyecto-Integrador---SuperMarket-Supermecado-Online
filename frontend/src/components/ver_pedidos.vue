<template>
  <h4 class="display-5">Lista de pedidos</h4>
  <div v-if="pedidos.length">
    <div v-for="pedido in pedidos" :key="pedido.id" class="mb-5 mt-5">
      <ul class="list-group">
        <li class="list-group-item list-group-item-dark"><strong>ID Pedido:</strong> {{ pedido.id }}</li>
        <li class="list-group-item list-group-item-dark"><strong>Dirección:</strong> {{ pedido.direccion }}</li>
        <li class="list-group-item list-group-item-dark"><strong>Horario:</strong> {{ pedido.horario }}</li>
        <li class="list-group-item list-group-item-dark"><strong>Fecha:</strong> {{ pedido.fecha }}</li>
        <li class="list-group-item list-group-item-dark"><strong>Comentarios:</strong> {{ pedido.comentarios }}</li>
        <li class="list-group-item list-group-item-dark"><strong>Método:</strong> {{ pedido.metodo }}</li>
        <li class="list-group-item list-group-item-dark"><strong>Total:</strong> ${{ pedido.total }}</li>
        <li class="list-group-item">
          <strong class="display-6">Productos:</strong>
          <ul class="list-group  list-group-item-dark mt-4">
            <li v-for="producto in pedido.productos" :key="producto.id" class="list-group-item">
              {{ producto.nombre }} - {{ producto.cantidad }} x ${{ producto.precio }}
            </li>
          </ul>
        </li>
        <div class="mt-4">
            <button @click="EliminarPedido(pedido)" class="btn btn-danger">
              Cancelar pedido
            </button>
        </div>
        
      </ul>
    </div>
  </div>
  <div v-else>
    <p>No hay pedidos para mostrar</p>
  </div>
   <div class='mt-3'>
        <p v-if="message" :class="messageClass">{{ message }}</p>
    </div>
    <router-link to="/inicio" class="btn btn-secondary mt-3">
          Volver al inicio
    </router-link>
</template>


<script>
import axios from 'axios'
export default{
    name: 'ListaPedidos',
    data(){
        return{
            pedidos: [],
            message: '',
            messageClass: ''
        }
    },
    async mounted() {
    try {
      const res = await axios.get('http://localhost:5000/api/get_pedidos', {
        withCredentials: true
      });
      this.pedidos = res.data
    } catch (err) {
      if (err.response && err.response.status === 401) {
        this.$router.push('/login');
      } else {
        console.error('Error al obtener productos:', err);
      }
    }
  },
  methods:{
    async EliminarPedido(pedido){
        const payload = {
            id_pedido : pedido.id

        }
        try {
            const respuesta = await axios.post('http://localhost:5000/api/eliminar_pedido', payload, { withCredentials: true });
            this.message = respuesta.data.message
            this.$router.push({path:'/inicio',query:{mensaje_ext: this.message}});  
          } catch (error) {
            console.error('Error al eliminar pedido:', error);
              this.messageClass = 'text-danger'
              this.message = 'Error al eliminar el pedido! [Error de servidor]'    
          }
        }
    }
}


</script>
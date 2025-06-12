<template>
    <h4 class="display-5">Lista de productos</h4>
    <div class = "mb-5 mt-5">
    <table v-if="productos && productos.length " class="table table-secondary table-sm">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Nombre</th>
          <th scope="col">Marca</th>
          <th scope="col">Descripción</th>
          <th scope="col">Precio</th>
          <th scope="col">Stock</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="producto in productos" :key="producto.id">
          <th scope="row">{{ producto.id }}</th>
          <td>{{ producto.nombre }}</td>
          <td>{{ producto.marca }}</td>
          <td>{{ producto.descripcion }}</td>
          <td>{{ producto.precio }}</td>
          <td>{{ producto.stock_temporal }}</td>
          <td>
            <button class="btn btn-primary" @click="incrementarStock(producto)" :disabled="producto.stock_temporal == 20">+</button>
          </td>
          <td><button class="btn btn-secondary" @click="decrementarStock(producto)">-</button>
          </td>
          <td><button class="btn btn-danger" @click="SeleccionarProducto(producto)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="spinner-border" role="status" v-else>
      <span class="visually-hidden">Cargando productos...</span>
    </div>
    <div class="mt-3 p-3">
            <button class="btn btn-primary" @click="guardarCambios()">Guardar cambios</button>
    </div>
    <div class='mt-3 '>
        <p v-if="message" :class="messageClass">{{ message }}</p>
    </div>
    <router-link to="/inicio_admin" class="btn btn-secondary mt-3">
        Atras</router-link>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name: 'administrarProductos',
    data(){
        return {
            productos: [],
            message: '',
            messageClass: ''

        }
    },
   async mounted() {
    try {
      const res = await axios.get('http://localhost:5000/api/get_productos', {
        withCredentials: true
      });
       this.productos = res.data.map(p => ({ ...p,
        stock_temporal: p.stock,
        eliminar: false
    }));
    } catch (err) {
      if (err.response && err.response.status === 401) {
        this.$router.push('/login_admin');
      } else {
        console.error('Error al obtener productos:', err);
      }
    }
  },
  methods:{
    incrementarStock(producto)
    {
    producto.stock_temporal++;
},
decrementarStock(producto)
{
if(producto.stock_temporal> 0)
{
    producto.stock_temporal--;
}
},
SeleccionarProducto(producto){
producto.eliminar = true
},
async guardarCambios() {
  const productosSeleccionados = this.productos
    .filter(p => p.stock_temporal > 0)
    .map(p => ({
      id: p.id,
      stock_temporal: p.stock_temporal
    }));

    const procutosSeleccionadosEliminar = this.productos
    .filter(p => p.eliminar == true)
    .map(p => ({
      id: p.id,
    }));

  const payload = {
    producto: productosSeleccionados,
    productos_eliminar: procutosSeleccionadosEliminar
  };

  try {
    const res = await axios.post('http://localhost:5000/api/actualizar_stock', payload, {
  withCredentials: true
});


    this.message = res.data.message;
    this.messageClass = 'text-success';
  } catch (error) {
    console.error(error);
    this.message = 'Error del servidor!';
    this.messageClass = 'text-danger';
  }
},
}
}


</script>
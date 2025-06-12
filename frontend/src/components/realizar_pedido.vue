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
          <th scope="col">Cantidad</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="producto in productos" :key="producto.id">
          <th scope="row">{{ producto.id }}</th>
          <td>{{ producto.nombre }}</td>
          <td>{{ producto.marca }}</td>
          <td>{{ producto.descripcion }}</td>
          <td>{{ producto.precio }}</td>
          <td>{{ producto.stock }}</td>
          <td>
            <button class="btn btn-primary" @click="incrementarCantidad(producto)"
            :disabled="producto.stock <= 0"> Cantidad: {{ producto.cantidad }}</button>
          </td>
          <td><button class="btn btn-secondary" @click="incrementarStock(producto)":disabled="producto.cantidad === 0">-</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="spinner-border" role="status" v-else>
      <span class="visually-hidden">Cargando productos...</span>
</div>
    </div>
    <div class="mt-3 d-flex justify-content-left">
      <p class="lead"><mark style="background-color:#ffc107"><strong>Total del pedido:</strong> ${{ totalPedido.toFixed(2) }}</mark></p>
    </div>
    <h4 class="display-5">Detalles de envío:</h4>
    <div class = "mt-4">
    <form @submit.prevent = "enviarPedido()">
            <div class="mb-3 d-flex align-items-center">
                <label for = "direccion" class="form-label me-2" style="min-width: 150px;">Dirección de envío: </label>
                <input type="text" class="form-control" v-model="direccion" placeholder="Direccion de envio" :class="{'form-control': true, 'is-invalid': errores.direccion}"/>
            </div>
            <div class="mb-3 d-flex align-items-center">
                <label for = "horario" class="form-label me-2" style="min-width: 150px;">Horario de preferencia: </label>
                <input type="text" class="form-control" v-model="horario" placeholder="horario de preferencia" :class="{'form-control': true, 'is-invalid': errores.horario}"/>
            </div>
            <div class="mb-3 d-flex align-items-center">
              <label for = "comentarios"class="form-label me-2" style="min-width: 150px;">Comentarios de entrega (Opcional):</label> 
              <textarea class="form-control"rows="5" v-model="comentarios" id="comentarios" name="comentarios"></textarea>
            </div>
         <div class="mb-3 d-flex align-items-center" >
          <label class="me-3" style="min-width: 150px;">Método de pago:</label>
          <div class="form-check form-switch me-5">
            <input class="form-check-input" type="radio" v-model="metodo" value="Transferencia" id="transferencia">
            <label class="form-check-label" for="transferencia">Transferencia</label>
          </div>
          <div class="form-check form-switch">
            <input class="form-check-input" type="radio" v-model="metodo" value="Efectivo" id="efectivo">
            <label class="form-check-label" for="efectivo">Efectivo</label>
          </div>
        </div>
        <p v-if="errores.metodo" class="text-danger ms-3">Por favor, seleccione un método de pago.</p>
        <div class="text-center mt-4 p-4">
          <button class="btn btn-primary">Realizar pedido</button>
        </div>
            
        </form>
        </div>
        <div class='mt-3 '>
            <p v-if="message" :class="messageClass">{{ message }}</p>
        </div>
        <router-link to="/inicio" class="btn btn-secondary mt-3">
          Volver al inicio
        </router-link>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TablaProductos',
  data() {
    return {
      productos: [],
      direccion: '',
      horario: '',
      comentarios: '',
      metodo: '',
      errores: {
        direccion: false,
        horario: false,
        metodo: false
      },
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
        precio: parseFloat(p.precio),
        cantidad: 0
    }));
    } catch (err) {
      if (err.response && err.response.status === 401) {
        this.$router.push('/login');
      } else {
        console.error('Error al obtener productos:', err);
      }
    }
  },
  computed: {
  totalPedido() {
    return this.productos.reduce((total, producto) => {
      return total + (producto.precio * producto.cantidad);
    }, 0);
  }
},
  methods: {

  incrementarCantidad(producto) {
    if (producto.stock > 0) {
      producto.cantidad++;
      producto.stock--; 
    }
  }
,

incrementarStock(producto){
  if (producto.cantidad > 0){
    producto.cantidad--;
    producto.stock++;
  }
},
  async enviarPedido() {
    this.errores = {
      direccion: !this.direccion,
      horario: !this.horario,
      metodo: !this.metodo
    };

  // Si hay algún error, no continuar
  if (this.errores.direccion || this.errores.horario || this.errores.metodo) {
    this.message = 'Por favor, completá todos los campos requeridos.';
    this.messageClass = 'text-danger';
    return;
  }
    const productosSeleccionados = this.productos
      .filter(p => p.cantidad > 0)
      .map(p => ({
        id: p.id,
        cantidad: p.cantidad,
        stock: p.stock
      }));

    if (productosSeleccionados.length === 0) {
        this.messageClass = 'text-danger'
        this.message = 'Selecciona al menos un producto!'
      return;
    }

    const payload = {
      productos: productosSeleccionados,
      direccion: this.direccion,
      horario: this.horario,
      comentarios: this.comentarios,
      metodo: this.metodo,
      total: this.totalPedido,
    };

    try {
      const respuesta = await axios.post('http://localhost:5000/api/pedidos', payload, { withCredentials: true });
      this.$router.push({path:'/inicio',query:{mensaje_ext: this.message}});  

    } catch (error) {
      console.error('Error enviando pedido:', error);
      this.messageClass = 'text-danger'
      this.message = 'Error al enviar el pedido! [Error de servidor]'    }
  }
}
}
</script>
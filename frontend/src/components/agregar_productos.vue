<template>
    <div class="Registro">
        <h2 class="display-5">Agregar un producto</h2>
        <div class = "p-4">
        <form @submit.prevent = "addProducto">
            <div class="mb-3 mt-3">
                <label for = "nombre_producto" class="form-label">Nombre del producto: </label>
                <input type="text" class="form-control" v-model="nombre_producto" placeholder="Nombre Producto" :class="{'form-control': true, 'is-invalid': errores.nombre_producto}"/>
            </div>
            <div class="mb-3">
                <label for = "marca" class="form-label">Marca: </label>
                <input type="text" class="form-control" v-model="marca" placeholder="Marca" :class="{'form-control': true, 'is-invalid': errores.marca}"/>
            </div>
            <div class="mb-3">
                <label for = "descripcion" class="form-label">Descripcion: </label>
                <input type="text" class="form-control" v-model="descripcion" placeholder="Descripcion" :class="{'form-control': true, 'is-invalid': errores.descripcion}"/>
            </div>
            <div class="mb-3">
                <label for = "precio" class="form-label">Precio: </label>
                <input type="text" class="form-control" v-model="precio" placeholder="Precio" :class="{'form-control': true, 'is-invalid': errores.precio}"/>
            </div>
            <div class="mb-3">
                <label for="stock" class="form-label">Stock: {{ stock }}</label>
                <input type="range" class="form-range" min="0" max="20" v-model="stock">
            </div>
            <div class="p-3">
                <button type="submit" class="btn btn-primary">Agregar Producto</button>
            </div>

        </form>
        </div>
        <div class='mt-3 p-3'>
            <p v-if="message" :class="messageClass">{{ message }}</p>
        </div>

        <router-link to="/inicio_admin" class="btn btn-secondary mt-3">
        Atras</router-link>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    data(){
        return{
            nombre_producto: '',
            marca: '',
            descripcion: '',
            precio: '',
            stock: '',
            errores:{
               nombre_producto: false,
               marca: false,
               descripcion: false,
               precio: false,
               stock: false,
               stock_zero: false

            },
            message: '',
            messageClass: ''
        }
    },
    methods:{
        async addProducto(){
            this.errores = {
                nombre_producto: !this.nombre_producto,
                marca: !this.marca,
                descripcion: !this.descripcion,
                precio: !this.precio,
                stock: !this.stock,
                stock_zero: this.stock == 0
            }

            if (this.errores.nombre_producto || this.errores.marca || this.errores.descripcion || this.errores.precio || this.errores.stock )
            {
                this.message = 'Por favor, completá todos los campos requeridos.';
                this.messageClass = 'text-danger';
                return;
            }

            if (this.errores.stock_zero)
            {
                this.message = 'Por favor,ingrese una cantidad de stock para el producto!.';
                this.messageClass = 'text-danger';
                return;
            }

            const payload = {
                nombre_producto: this.nombre_producto,
                marca: this.marca,
                descripcion: this.descripcion,
                precio: this.precio,
                stock: this.stock
            };

            try{
                 const response = await axios.post('http://localhost:5000/api/agregar_producto', payload, {withCredentials: true

                 });

                    this.message = response.data.message
                    this.messageClass = 'text-success'

                   
                    if (response.data.message === 'Producto agregado correctamente!')

                    {
                        this.nombre_producto = ''
                        this.marca = ''
                        this.descripcion = ''
                        this.precio = ''
                        this.stock  = ''

                    }
                    
            } catch (error) {
                console.error(error)
                this.messageClass = 'text-danger'
                this.message = 'Error del servidor!' 
            }
        }
    }
}
</script>
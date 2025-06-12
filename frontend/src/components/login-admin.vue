<template>
    <div class = "Login d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 shadow bg-light bg-opacity-75" style="min-width: 320px; max-width: 400px;">
        <h2 class="mb-4 text-center">Inicio de sesión de admin</h2>
        <form @submit.prevent = "logearAdmin">
            <div class="mb-3 mt-3">
                <label for = "correo" class="form-label">Correo electrónico: </label>
                <input type="text" class="form-control" v-model="correo" placeholder="Correo electrónico" :class="{'form-control': true, 'is-invalid': errores.correo}"/>
            </div>
            <div class="mb-3">
                <label for = "password" class="form-label">Código de autorización: </label>
                <input type="password" class="form-control" v-model="codigo" placeholder="Codigo de autorización" :class="{'form-control': true, 'is-invalid': errores.codigo}"/>
            </div>
            <div class="mb-4 p-2">
                <button type="submit" class="btn btn-primary">Ingresar</button>
            </div>
        </form>
        <div class='mt-3'>
            <p v-if="message" :class="messageClass">{{ message }}</p>
        </div>
        

    </div>
    </div>
     <router-link to="/" class="btn btn-secondary mt-3">
        Atras
    </router-link>
</template>
 
<script>
import axios from 'axios'

export default{
    data(){
        return{
            correo: '',
            codigo: '',
            errores: {
                correo: false,
                codigo: false
            },
            message: '',
            messageClass: ''

        }
    },
    methods: {
        async logearAdmin(){
            this.errores = {
                correo: !this.correo,
                codigo: !this.codigo
            }
            if (this.errores.correo || this.errores.codigo) {
                this.message = 'Por favor, completá todos los campos requeridos.';
                this.messageClass = 'text-danger';
                return;
            }
            try{
                 const response = await axios.post('http://localhost:5000/api/login_admin', {
                    correo: this.correo,
                    codigo: this.codigo
                    },{  withCredentials: true  // MUY IMPORTANTE para que el navegador acepte la cookie de sesión
                    })
                this.messageClass = 'text-success'
                this.message = response.data.message

                if (response.data.message == 'Ingresó correctamente!'){
                    this.$router.push('/inicio_admin');  // Asegúrate de que /home esté definido en el router

                }
                else{
                         this.messageClass = 'text-danger'
                         this.message = response.data.message
                    }
            } catch (error) {
                console.error(error)
                this.messageClass = 'text-danger'
                this.message = "Error del servidor!"
            }
        }
    }
}
</script>

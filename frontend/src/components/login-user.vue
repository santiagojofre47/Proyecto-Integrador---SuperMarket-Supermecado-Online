<template>
    <div class = "Login d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 shadow bg-light bg-opacity-75" style="min-width: 320px; max-width: 400px;">
            <h2 class="mb-4 text-center">Inicio de sesión de Usuario</h2>
            <form @submit.prevent = "logearUsuario">
                <div class="mb-3 mt-3">
                <label for = "correo" class="form-label">Correo electrónico: </label>
                <input type="text" class="form-control" v-model="correo" placeholder="Correo electrónico" :class="{'form-control': true, 'is-invalid': errores.correo}"/>
            </div>
            <div class="mb-3">
                <label for = "password" class="form-label">Contraseña: </label>
                <input type="password" class="form-control" v-model="password" placeholder="Contraseña" :class="{'form-control': true, 'is-invalid': errores.password}"/>
            </div>
            <div class="p-3">
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
            password: '',
            errores:{
                correo: false,
                password: false
            },
            message: '',
            messageClass: ''

        }
    },
    methods: {
        async logearUsuario(){
            this.errores = {
                correo: !this.correo,
                password: !this.password
            }
            
            if(this.errores.correo || this.errores.password)
            {
                this.message = 'Por favor, completá todos los campos requeridos.';
                this.messageClass = 'text-danger';
                return;
            }
            try{
                 const response = await axios.post('http://localhost:5000/api/login', {
                    correo: this.correo,
                    password: this.password
                    },{  withCredentials: true  // MUY IMPORTANTE para que el navegador acepte la cookie de sesión
                    })
                this.message = response.data.message

                if (response.data.message == 'Ingresó correctamente!'){
                    this.$router.push({path:'/inicio',query:{mensaje_ext: this.message}}); 
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
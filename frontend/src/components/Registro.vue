<template>
    <div class="Registro">
        <h2 class="display-5">Registro de usuario</h2>
        <div class = "p-4">
        <form @submit.prevent = "registrarUsuario">
            <div class="mb-3 mt-3">
                <label for = "nombre" class="form-label">Nombre: </label>
                <input type="text" class="form-control" v-model="nombre" placeholder="Nombre" :class="{'form-control': true, 'is-invalid': errores.nombre}"/>
            </div>
            <div class="mb-3">
                <label for = "apellido" class="form-label">Apellido: </label>
                <input type="text" class="form-control" v-model="apellido" placeholder="Apellido" :class="{'form-control': true, 'is-invalid': errores.apellido}"/>
            </div>
            <div class="mb-3">
                <label for = "dni" class="form-label">DNI: </label>
                <input type="text" class="form-control" v-model="dni" placeholder="DNI" :class="{'form-control': true, 'is-invalid': errores.dni}"/>
            </div>
            <div class="mb-3">
                <label for = "correo" class="form-label">Correo electrónico: </label>
                <input type="text" class="form-control" v-model="correo" placeholder="Correo electrónico" :class="{'form-control': true, 'is-invalid': errores.correo}"/>
            </div>
            <div class="mb-3">
                <label for = "pasword" class="form-label">Contraseña: </label>
                <input type="password" class="form-control" v-model="password" placeholder="Password" :class="{'form-control': true, 'is-invalid': errores.password }"/>
            </div>

            <div class="p-3">
                <button type="submit" class="btn btn-primary">Registrarse</button>
            </div>

        </form>
        </div>
        <div class='mt-3 p-3'>
            <p v-if="message" :class="messageClass">{{ message }}</p>
        </div>

        <router-link to="/" class="btn btn-secondary mt-3">
        Atras</router-link>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    data(){
        return{
            nombre: '',
            apellido: '',
            dni: '',
            correo: '',
            password: '',
            errores:{
               nombre: false,
               apellido: false,
               dni: false,
               correo: false,
               password: false,
            },
            message: '',
            messageClass: ''
        }
    },
    methods:{
        async registrarUsuario(){
            
            const strictEmailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            const PassworRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:'",.<>/?\\|`~]).+$/;
            const OnlyNumbersRegex = /^\d+$/;
            const OnlyLettersRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+$/;


            this.errores = {
                nombre: !this.nombre,
                apellido: !this.apellido,
                dni: !this.dni,
                correo: !this.correo,
                password: !this.password
            }

            if (this.errores.nombre || this.errores.apellido || this.errores.dni || this.errores.correo || this.errores.password )
            {
                this.message = 'Por favor, completá todos los campos requeridos.';
                this.messageClass = 'text-danger';
                return;
            }

            if (!strictEmailRegex.test(this.correo))
            {
                this.message = 'El formato de correo es inválido! Debe contener @ y un .';
                this.messageClass = 'text-danger';
                return;

            }

            if(!PassworRegex.test(this.password)){
                this.message = "La contraseña debe tener al menos una mayúscula, un número y un carácter especial";
                this.messageClass = 'text-danger';
                return;
            }

            if(!OnlyNumbersRegex.test(this.dni)){
                this.message = "El DNI solo debe contener números!";
                this.messageClass = 'text-danger';
                return;
            }

            if(!OnlyLettersRegex.test(this.nombre) || !OnlyLettersRegex.test(this.apellido))
            {
                this.message = "El nombre solo debe contener letras!";
                this.messageClass = 'text-danger';
                return;
            }

            
            if(!this.password >= 5 && !this.password <= 20)
            {
                this.message = 'La contraseña debe tener entre 5 y 20 caracteres.';
                this.messageClass = 'text-danger';
                return;
            }

            try{
                 const response = await axios.post('http://localhost:5000/api/registro', {
                    nombre: this.nombre,
                    apellido: this.apellido,
                    dni: this.dni,
                    correo: this.correo,
                    password: this.password
                    },{withCredentials: true})
                    this.message = response.data.message
                   
                    if (response.data.message == 'Usuario creado correctamente!')
                    {
                        this.$router.push({path:'/inicio',query:{mensaje_ext: this.message}});  


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
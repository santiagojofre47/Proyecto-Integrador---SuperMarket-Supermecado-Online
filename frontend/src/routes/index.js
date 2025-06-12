import axios from 'axios'
import {createRouter, createWebHistory} from 'vue-router'
import inicio from '../components/inicio.vue'
import Registro from '../components/Registro.vue'
import loginUser from '../components/login-user.vue'
import loginAdmin from '../components/login-admin.vue'
import inicio_ingresado from '../components/inicio_ingresado.vue'
import realizar_pedido from '../components/realizar_pedido.vue'
import ver_pedidos from '../components/ver_pedidos.vue'
import cerrar_sesion from '../components/cerrar_sesion.vue'
import inicio_admin from '../components/inicio_admin.vue'
import cerrar_sesion_admin from '../components/cerrar_sesion_admin.vue'
import agregar_productos from '../components/agregar_productos.vue'
import administrar_productos from '../components/administrar_productos.vue'

const ifNotAuthenticated = async (to, from, next) => {
  try {
    await axios.get('http://localhost:5000/api/check_auth', { withCredentials: true });
      next({
      path: '/inicio',
      query: { mensaje_ext: 'Usted ya ha iniciado sesión!"' }
    });
  } catch (err) {
    next();
  }
};

const routes = [
    {
        path: '/',
        name: 'Home',
        component: inicio,
    },
    {
        path: '/registro',
        name: 'Registro',
        component: Registro,
        beforeEnter: ifNotAuthenticated


    },
    {
        path: '/login',
        name: 'Login',
        component: loginUser,
        beforeEnter: ifNotAuthenticated

    },
    {
        path: '/login_admin',
        name: 'login2',
        component: loginAdmin

    },
    {
        path: '/inicio',
        name: 'Inicio',
        component:inicio_ingresado

    },
    {
        path: '/realizar_pedido',
        name: 'realizar_pedido',
        component:realizar_pedido
        
    },
    {
        path: '/ver_pedidos',
        name: 'ver_pedidos',
        component: ver_pedidos
    },
    {
        path: '/cerrar_sesion',
        name: 'cerrar_sesion',
        component: cerrar_sesion
    },
    {
        path: '/inicio_admin',
        name: 'inicio_admin',
        component: inicio_admin
    },
    {
        path: '/cerrar_sesion_admin',
        name: 'cerrar_sesion_admin',
        component: cerrar_sesion_admin
    },
    {
        path: '/agregar_productos',
        name: 'agregar_productos',
        component: agregar_productos
    },
    {
        path: '/administrar_productos',
        name: 'administrar_productos',
        component: administrar_productos
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
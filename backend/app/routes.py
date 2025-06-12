from flask import Blueprint, jsonify, request
from app.models import verificar,crear_usuario,obtener_usuario_por_correo,obtener_admin_por_correo,get_productos,crear_pedido,get_pedidos_con_productos,borrar_pedido,guardar_ultconexion,obtener_ultconexion,guardar_ultconexion_admin,obtener_ultconexion_admin,add_producto,update_stock,eliminar_productos
from flask_login import login_user, login_required, current_user,logout_user
from datetime import datetime
api = Blueprint('api',__name__)

@api.route('/api/data')
def get_data():
    mensaje = verificar()
    print(mensaje)
    return jsonify({'message':mensaje})

@api.route('/api/inicio')
@login_required
def mensaje():
    ultima_conexion = obtener_ultconexion(current_user.id)
    if ultima_conexion:
        return jsonify(({'message':f'Bienvenido <strong>{current_user.nombre}</strong> tu ultima conexión fue el <strong>{ultima_conexion}</strong>!'}))
    else:
         return jsonify(({'message':f'Bienvenido <strong>{current_user.nombre}</strong> a nuestro supermercado online!'}))


@api.route('/api/inicio_admin')
@login_required
def mensaje_admin():
    ultima_conexion = obtener_ultconexion_admin(current_user.id)
    return jsonify(({'message':f'Bienvenido administrador <strong>{current_user.nombre}</strong> tu ultima conexión fue el <strong>{ultima_conexion}</strong>!'}))

@api.route('/api/registro', methods = ['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    dni = data.get('dni')
    correo = data.get('correo')
    password = data.get('password')
    msj,usuario = crear_usuario(nombre,apellido,dni,correo,password)
    login_user(usuario)
    return jsonify({'message':msj})

@api.route('/api/login', methods=['GET','POST'])
def ingresar_usuario():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')
    usuario = obtener_usuario_por_correo(correo)
    if usuario:
        if usuario.password == password:
            login_user(usuario)
            return jsonify({'message':'Ingresó correctamente!'})
        else:
            return jsonify({'message':'Contraseña Incorrecta!'})
    else:
        return jsonify({'message':'Usuario no encontrado!'})

@api.route('/api/login_admin', methods=['GET','POST'])
def ingresar_administrador():
    data = request.get_json()
    correo = data.get('correo')
    codigo = data.get('codigo')
    administrador = obtener_admin_por_correo(correo)
    if administrador:
        if administrador.codigo == codigo:
            login_user(administrador)
            return jsonify({'message':'Ingresó correctamente!'})
        else:
            return jsonify({'message':'Contraseña Incorrecta!'})
    else:
        return jsonify({'message':'Usuario no encontrado!'})

@api.route('/api/get_productos', methods=['GET','POST'])
@login_required
def obtener_productos():
    productos = get_productos()
    return jsonify(productos)
    

@api.route('/api/pedidos', methods=['GET','POST'])
@login_required
def tomar_pedido():
    data = request.get_json()
    productos = data.get('productos')
    direccion = data.get('direccion')
    horario = data.get('horario')
    comentarios = data.get('comentarios')
    total = data.get('total')
    metodo = data.get('metodo')
    usuario_id = current_user.id
    fecha = datetime.now()
    crear_pedido(productos,usuario_id,direccion,horario,fecha,comentarios,metodo,total)
    return jsonify({'message':'Pedido realizado con éxito'})

@api.route('/api/get_pedidos',methods=['GET','POST'])
@login_required
def get_pedidos():
    pedidos = get_pedidos_con_productos(current_user.id)
    return jsonify(pedidos)

@api.route('/api/eliminar_pedido',methods=['GET','POST'])
@login_required
def eliminar_pedido():
    data = request.get_json()
    pedido_id = data.get('id_pedido')
    if not pedido_id:
        print('Error')
    else:
        borrar_pedido(pedido_id)

    return jsonify({'message':'Pedido eliminado con éxito!'})

@api.route('/api/logout', methods=['GET','POST'])
@login_required
def logout():
    guardar_ultconexion(current_user.id,datetime.now()
)
    logout_user()
    return jsonify({'message':'Sesión cerrada con éxito'})

@api.route('/api/logout_admin', methods=['GET','POST'])
@login_required
def logout_admin():
    guardar_ultconexion_admin(current_user.id,datetime.now())
    logout_user()
    return jsonify({'message':'Sesión cerrada con éxito'})

@api.route('/api/check_auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True}), 200
    return jsonify({'authenticated': False}), 401

@api.route('/api/agregar_producto', methods=['POST', 'OPTIONS'])
@login_required
def agregar_producto():
    if request.method == 'OPTIONS':
        return '', 200  # responder a la preflight
    
    data = request.get_json()
    nombre_producto = data['nombre_producto']
    marca = data['marca']
    descripcion = data['descripcion']
    precio = data['precio']
    stock = data['stock']
    msj = add_producto(nombre_producto, marca, descripcion, precio, stock)
    return jsonify({'message': msj})

@api.route('/api/actualizar_stock', methods=['POST','OPTIONS'])
@login_required
def actualizar_stock():
    if request.method == 'OPTIONS':
        return '', 200  # responder a la preflight
    
    data = request.get_json()
    productos=data.get('producto',[])
    productos_eliminar = data.get('productos_eliminar',[])
    msj = ''
    if productos:
        msj = update_stock(productos)
    if productos_eliminar:
        msj = eliminar_productos(productos_eliminar)
    return jsonify({'message':msj})

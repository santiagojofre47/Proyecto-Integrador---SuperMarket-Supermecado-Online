from models.usuario import Usuario
from models.admin import Admin
from . import mysql
from MySQLdb.cursors import DictCursor

def crear_usuario(nombre,apellido,dni,correo,password):
    cursor = mysql.connection.cursor()
    cursor.execute('''
    INSERT INTO usuarios (nombre, apellido, dni, correo, password)
    VALUES (%s, %s, %s, %s, %s)
''', (nombre, apellido, dni, correo, password))
    mysql.connection.commit()
    cursor.close()
    usuario = obtener_usuario_por_correo(correo)
    return f'Usuario creado correctamente!',usuario

def obtener_usuario_por_correo(correo):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
    datos = cursor.fetchone()
    cursor.close()

    if datos:
        return Usuario(id=datos[0], nombre=datos[1], correo=datos[4], password=datos[5])
    return None

def obtener_usuario_por_id(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    datos = cursor.fetchone()
    cursor.close()

    if datos:
        return Usuario(id=datos[0], nombre=datos[1], correo=datos[4], password=datos[5])
    return None

def obtener_admin_por_correo(correo):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM administradores WHERE correo = %s', (correo,))
    datos = cursor.fetchone()
    cursor.close()
    if datos:
        return Admin(id=datos[0], correo=datos[3], codigo=datos[4])
    return None

def get_productos():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos')
    datos = cursor.fetchall()
    cursor.close()
    resultado = [{'id':d[0],'nombre':d[1],'marca':d[2],'descripcion':d[3],'precio':d[4],'stock':d[5]}
                  for d in datos]
    return resultado

def crear_pedido(productos,usuario_id,direccion,horario,fecha,comentarios,metodo,total):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO pedidos (usuario_id,direccion,horario,fecha,comentarios,metodo_pago,importe_total) VALUES(%s, %s, %s, %s, %s, %s, %s)',
                   (usuario_id,direccion,horario,fecha,comentarios,metodo,total))
    pedido_id = cursor.lastrowid
    for producto in productos:
        cursor.execute('INSERT INTO pedidos_detalles (pedido_id, producto_id, cantidad) VALUES (%s, %s, %s)',
                       (pedido_id, producto['id'], producto['cantidad']))
        cursor.execute('UPDATE productos SET stock=%s WHERE id=%s',(producto['stock'],producto['id']))

    mysql.connection.commit()
    cursor.close()

def get_pedidos_con_productos(usuario_id):
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT 
            p.id AS pedido_id,
            p.direccion,
            p.horario,
            p.fecha,
            p.comentarios,
            p.metodo_pago,
            p.importe_total,
            pr.id AS producto_id,
            pr.nombre,
            pr.precio,
            pd.cantidad
        FROM pedidos p
        JOIN pedidos_detalles pd ON p.id = pd.pedido_id
        JOIN productos pr ON pd.producto_id = pr.id
        WHERE p.usuario_id = %s
        ORDER BY p.id DESC
    """, (usuario_id,))
    
    rows = cursor.fetchall()
    cursor.close()

    pedidos = {}
    for row in rows:
        pid = row['pedido_id']
        if pid not in pedidos:
            pedidos[pid] = {
                'id': pid,
                'direccion': row['direccion'],
                'horario': row['horario'],
                'fecha': row['fecha'],
                'comentarios': row['comentarios'],
                'metodo': row['metodo_pago'],
                'total': row['importe_total'],
                'productos': []
            }
        pedidos[pid]['productos'].append({
            'id': row['producto_id'],
            'nombre': row['nombre'],
            'precio': float(row['precio']),
            'cantidad': row['cantidad']
        })
        print(list(pedidos.values()))

    return list(pedidos.values())

def borrar_pedido(id_pedido):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id=%s" ,(id_pedido,) )
    cursor.execute("DELETE FROM pedidos_detalles WHERE id=%s", (id_pedido,) )
    mysql.connection.commit()
    cursor.close()

def guardar_ultconexion(id_usuario,fecha):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET ultima_conexion=%s WHERE id=%s", (fecha,id_usuario))
    mysql.connection.commit()
    cursor.close()
    print('Ultima conexión guardada')
    
def guardar_ultconexion_admin(id_admin,fecha):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE administradores SET ultima_conexion=%s WHERE id=%s", (fecha,id_admin))
    mysql.connection.commit()
    cursor.close()
    print('Ultima conexión guardada')
    
def obtener_ultconexion(id_usuario):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ultima_conexion FROM usuarios WHERE id = %s", (id_usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    if resultado and resultado[0]:
        ultima_conexion = resultado[0]
        return ultima_conexion.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return "Sin conexión previa"
    
def obtener_ultconexion_admin(id_admin):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ultima_conexion FROM usuarios WHERE id = %s", (id_admin,))
    resultado = cursor.fetchone()
    cursor.close()
    if resultado and resultado[0]:
        ultima_conexion = resultado[0]
        return ultima_conexion.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return "Sin conexión previa"

def add_producto(nombre_producto, marca, descripcion, precio, stock):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO productos (nombre,marca,descripcion,precio,stock) VALUES (%s,%s,%s,%s,%s)", (nombre_producto,marca,descripcion,precio,stock))
    mysql.connection.commit()
    cursor.close()
    return f'Producto agregado correctamente!'

def update_stock(productos):
    cursor = mysql.connection.cursor()
    for p in productos:
        cursor.execute('UPDATE productos set stock=%s where id=%s', (p['stock_temporal'], p['id']))
    mysql.connection.commit()
    cursor.close()
    return f'Stock actualizado!'

def eliminar_productos(productos):
    cursor = mysql.connection.cursor()
    for p in productos:
        cursor.execute('DELETE FROM productos where id=%s', (p['id'],))
    mysql.connection.commit()
    cursor.close()
    return f'Productos eliminados'

def verificar():
    return 'Mensaje enviado desde Flask!'
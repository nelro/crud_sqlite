from flask import  Flask, render_template, request, redirect, url_for
import sqlite3

#creando la BD almacen
conexionBD =  sqlite3.connect('almacen.db')

#creamos  un cursor
cursor = conexionBD.cursor()

#creamos la tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos(
        id_pro integer  PRIMARY KEY AUTOINCREMENT,
        descripcion  text not null,
        cantidad  integer not null,
        precio  real not null
    )
''')
#insertamos un dato
#cursor.execute("INSERT INTO productos (descripcion, cantidad, precio) VALUES ('sadasd',8,7)")

#guardamos los cambios
conexionBD.commit()

#salimos de la conexion d ela  BD
conexionBD.close()




app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#funcion para mostar datos
#@app.route('/mostrar')
def mostrar_pro():
    conexionBD =  sqlite3.connect('almacen.db')
    cursor = conexionBD.cursor()
    cursor.execute("SELECT * FROM productos")
    datos_pro = cursor.fetchall()
    #if  datos_pro:
    producto_env=[]
    for item in datos_pro:
        producto_capt = {
            'id_pro':item[0],
            'descripcion':item[1],
            'cantidad':item[2],
            'precio':item[3]
        }
        producto_env.append(producto_capt)
    
    #salimos de la conexion d ela  BD
    conexionBD.close()
    
    return producto_env

@app.route('/eliminar/<int:id_pro>')
def eliminar(id_pro):
    
    # Conexión a la base de datos
    conexionBD = sqlite3.connect('almacen.db')
    cursor = conexionBD.cursor()
    
    # Ejecutamos la consulta SQL para eliminar el producto con el id_pro
    cursor.execute("DELETE FROM productos WHERE id_pro = ?", (id_pro,))
    
    # Confirmamos los cambios
    conexionBD.commit()
    
    # Cerramos la conexión a la base de datos
    conexionBD.close()
    #actualizamos la tabla
    productos=mostrar_pro()

    #retornamos al formulario
    return render_template('productos.html',productos=productos)

@app.route('/productos')
def productos():
    
    productos=mostrar_pro()

    return  render_template('productos.html',productos=productos)

@app.route('/nuevo_producto')
def nuevo_producto():
    return render_template('nuevo_producto.html')

@app.route('/editar_producto')
def editar_producto():
    return render_template('editar_producto.html')
    


if  __name__ == '__main__':
    app.run(debug=True)


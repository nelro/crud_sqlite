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


@app.route('/productos')
def productos():
    
    productos=mostrar_pro()

    return  render_template('productos.html',productos=productos)

@app.route('/nuevo_producto',methods=['POST','GET'])
def nuevo_producto():

    #almacenanmos lso datos recividos desde el form,ulario
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        #realizando la conexion a la base de datos
        conexionBD =  sqlite3.connect('almacen.db')
        cursor = conexionBD.cursor()

        #insertamos los datos en la base de datos medainte la consulta
        cursor.execute("INSERT INTO productos (descripcion,cantidad,precio) VALUES (?,?,?)",(descripcion,cantidad,precio))
    
        #guardanmos la consulta y lo  cerramos
        conexionBD.commit()
        conexionBD.close()

        #ahora retornamos a  la pagina de productos
        return redirect(url_for('productos'))

    return render_template('nuevo_producto.html')

@app.route('/capturar_producto/<int:id_pro>',methods=['GET'])
def capturar_producto(id_pro):
    #realizamos la conexion a la BD 
    conexionBD =  sqlite3.connect('almacen.db')
    cursor = conexionBD.cursor()
    #capturamos el producto a editar para poder  mostrarlo en el formulario
    #mediante una consulta 
    cursor.execute("SELECT * FROM productos WHERE id_pro = ?",(id_pro,))
    
    #guardamos los datos encontrados  en la variable producto_capt
    producto_capt = cursor.fetchone()

    #ceramos la coneccion a la BD
    conexionBD.close()

    #alamcenamos el producto en un  diccionario para poder enviarlo al formulario editar
    #realizamos un if para ver si hay elemtos  en el producto_capt

    if  producto_capt:
        enviar_datos_pro = {
            'id_pro': producto_capt[0],
            'descripcion': producto_capt[1],
            'cantidad': producto_capt[2],
            'precio': producto_capt[3]
        }
        #realizamos el evnvio al formulario  editar
        return render_template('editar_producto.html',enviar_datos_pro=enviar_datos_pro)
    else:
        #retornamos al mormulario  de productos
        return redirect(url_for('productos'))


#creamos la funcon para poder modificar los datos que caturamos  en el formulario editar
@app.route('/editar_producto/<int:id_pro>',methods=['POST'])
def editar_producto(id_pro):
    #realizamos al obtencion de los datos  del formulario editar
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    #realizamos la conexion a la BD
    conexionBD =  sqlite3.connect('almacen.db')
    cursor = conexionBD.cursor()

    #realizamos la consulta para poder  modificar los datos en la BD
    cursor.execute("UPDATE productos SET descripcion = ?, cantidad = ?, precio = ? WHERE id_pro =?",(descripcion,cantidad,precio,id_pro))
    
    #guardamos cabios de la consulta ejecutada y cerramos BD
    conexionBD.commit()
    conexionBD.close()

    #ahor avolvemos a la pagina de productos
    return redirect(url_for('productos'))

    
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
    

    return redirect(url_for('productos'))
  


if  __name__ == '__main__':
    app.run(debug=True)


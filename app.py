from flask import  Flask, render_template, request, redirect, url_for
import sqlite3

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return  render_template('productos.html')

@app.route('/nuevo_producto')
def nuevo_producto():
    return render_template('nuevo_producto.html')

@app.route('/editar_producto')
def editar_producto():
    return render_template('editar_producto.html')
    


if  __name__ == '__main__':
    app.run(debug=True)


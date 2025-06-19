from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "inventario.db"

def ejecutar_sql(query, params=(), consultar=False):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if consultar:
            return cursor.fetchall()
        conn.commit()

@app.before_first_request
def crear_tabla():
    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
    )
    """)

@app.route('/')
def index():
    productos = ejecutar_sql("SELECT * FROM productos", consultar=True)
    return render_template("index.html", productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        ejecutar_sql("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                     (nombre, cantidad, precio))
        return redirect('/')
    return render_template("agregar.html")

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        ejecutar_sql("UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
                     (nombre, cantidad, precio, id))
        return redirect('/')
    producto = ejecutar_sql("SELECT * FROM productos WHERE id=?", (id,), consultar=True)[0]
    return render_template("editar.html", producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    ejecutar_sql("DELETE FROM productos WHERE id=?", (id,))
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

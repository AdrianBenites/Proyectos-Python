from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def buscar_producto_por_codigo(codigo):
    with sqlite3.connect('productos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cantidad, precio FROM productos WHERE codigo=?", (codigo,))
        return cursor.fetchone()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    codigo = data['codigo']
    producto = buscar_producto_por_codigo(codigo)
    if producto:
        return jsonify({
            "nombre": producto[0],
            "cantidad": producto[1],
            "precio": producto[2]
        })
    return jsonify({"error": "Producto no encontrado"})

if __name__ == '__main__':
    app.run(debug=True)

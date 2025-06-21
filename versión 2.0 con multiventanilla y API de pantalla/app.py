from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "turnos.db"

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
    CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        punto TEXT DEFAULT '',
        estado TEXT DEFAULT 'pendiente'
    )
    """)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tomar_turno', methods=['POST'])
def tomar_turno():
    hoy = datetime.today().strftime("%Y-%m-%d")
    ultimo = ejecutar_sql("SELECT MAX(numero) FROM turnos WHERE fecha=?", (hoy,), consultar=True)[0][0]
    nuevo = 1 if ultimo is None else ultimo + 1
    ejecutar_sql("INSERT INTO turnos (numero, fecha) VALUES (?, ?)", (nuevo, hoy))
    return render_template("index.html", turno_asignado=nuevo)

@app.route('/operador', methods=['GET', 'POST'])
def operador():
    hoy = datetime.today().strftime("%Y-%m-%d")
    turno_actual = ejecutar_sql("SELECT id, numero FROM turnos WHERE estado='pendiente' AND fecha=? ORDER BY numero ASC LIMIT 1", (hoy,), consultar=True)
    if request.method == 'POST':
        punto = request.form.get("punto")
        id_turno = request.form.get("id_turno")
        ejecutar_sql("UPDATE turnos SET estado='atendido', punto=? WHERE id=?", (punto, id_turno))
        return redirect('/operador')
    return render_template("operador.html", turno=turno_actual[0] if turno_actual else None)

@app.route('/pantalla')
def pantalla():
    return render_template("pantalla.html")

@app.route('/api/turno_actual')
def api_turno_actual():
    hoy = datetime.today().strftime("%Y-%m-%d")
    turno_actual = ejecutar_sql("SELECT numero, punto FROM turnos WHERE estado='atendido' AND fecha=? ORDER BY id DESC LIMIT 1", (hoy,), consultar=True)
    if turno_actual:
        return jsonify({"numero": turno_actual[0][0], "punto": turno_actual[0][1]})
    return jsonify({"numero": "-", "punto": "-"})

@app.route('/historial')
def historial():
    hoy = datetime.today().strftime("%Y-%m-%d")
    turnos = ejecutar_sql("SELECT numero, punto, estado FROM turnos WHERE fecha=?", (hoy,), consultar=True)
    return render_template("historial.html", turnos=turnos, fecha=hoy)

if __name__ == '__main__':
    app.run(debug=True)

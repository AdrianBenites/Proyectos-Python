from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']
        
        # Guardar en archivo (opcional)
        with open('mensajes.txt', 'a', encoding='utf-8') as f:
            f.write(f"{nombre} - {correo} - {mensaje}\n")

        return render_template("gracias.html", nombre=nombre)
    return render_template("formulario.html")

if __name__ == '__main__':
    app.run(debug=True)




from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        # Crear PDF en memoria
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.setTitle("Formulario recibido")

        pdf.drawString(100, 750, f"Nombre: {nombre}")
        pdf.drawString(100, 730, f"Correo: {correo}")
        pdf.drawString(100, 710, "Mensaje:")
        text_obj = pdf.beginText(100, 690)
        for linea in mensaje.splitlines():
            text_obj.textLine(linea)
        pdf.drawText(text_obj)
        pdf.save()

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="formulario.pdf", mimetype='application/pdf')

    return render_template("index.html")

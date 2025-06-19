from flask import Flask, render_template, request
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    contenido = ""
    tipo = ""
    error = ""

    if request.method == 'POST':
        archivo = request.files['archivo']
        tipo_archivo = archivo.filename.split('.')[-1].lower()

        try:
            if tipo_archivo == 'json':
                data = json.load(archivo)
                contenido = json.dumps(data, indent=4, ensure_ascii=False)
                tipo = "JSON"
            elif tipo_archivo == 'xml':
                tree = ET.parse(archivo)
                root = tree.getroot()
                contenido = mostrar_xml(root)
                tipo = "XML"
            else:
                error = "Tipo de archivo no soportado. Solo JSON o XML."
        except Exception as e:
            error = f"Error al procesar el archivo: {str(e)}"

    return render_template("resultado.html", contenido=contenido, tipo=tipo, error=error)

def mostrar_xml(elemento, nivel=0):
    salida = "  " * nivel + f"<{elemento.tag}"
    if elemento.attrib:
        salida += " " + " ".join(f'{k}="{v}"' for k, v in elemento.attrib.items())
    salida += ">\n"

    for child in elemento:
        salida += mostrar_xml(child, nivel + 1)

    if elemento.text and elemento.text.strip():
        salida += "  " * (nivel + 1) + elemento.text.strip() + "\n"

    salida += "  " * nivel + f"</{elemento.tag}>\n"
    return salida

if __name__ == '__main__':
    app.run(debug=True)

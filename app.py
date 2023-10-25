from flask import Flask, jsonify, request
from flask_cors import CORS

from controladores.funciones import funciones

app = Flask(__name__)
CORS(app)

func = funciones()

@app.route('/grabarMensajes', methods=['POST'])
def subir_archivo_mensajes():
    if 'file' not in request.files:
        return jsonify({
            'message': 'No hay ningun archivo'
        })

    file = request.files['file']

    archivo = file

    func.cargar_archivo_mensajes(archivo)

    return jsonify({
        'message': 'Archivo cargado correctamente.'
    })

@app.route('/grabarConfiguracion', methods=['POST'])
def subir_archivo_diccionario():
    if 'file' not in request.files:
        return jsonify({
            'message': 'No hay ningun archivo'
        })

    file = request.files['file']

    archivo = file

    func.cargar_archivo_diccionario(archivo)

    return jsonify({
        'message': 'Archivo cargado correctamente.'
    })

@app.route("/devolverHashtags", methods = ['GET'])
def obtener_hashtags():
    fecha_in = request.form.get('fecha_in')
    fecha_fin = request.form.get('fecha_fin')
    respuesta = func.consultar_hashtags(fecha_in, fecha_fin)

    return jsonify({
        'fecha_inicio': fecha_in,
        'fecha_fin': fecha_fin,
        'hashtags': respuesta
    })

@app.route("/devolverMenciones", methods = ['GET'])
def obtener_menciones():
    fecha_in = request.form.get('fecha_in')
    fecha_fin = request.form.get('fecha_fin')
    respuesta = func.consultar_menciones(fecha_in, fecha_fin)

    return jsonify({
        'fecha_inicio': fecha_in,
        'fecha_fin': fecha_fin,
        'menciones': respuesta
    })

if __name__ == '__main__':
    app.run(threaded = True, port = 5000, debug = True)
from flask import Flask, jsonify, request
from flask_cors import CORS

from controladores.funciones import funciones

app = Flask(__name__)
CORS(app)

func = funciones()

@app.route('/subir-archivo-mensajes', methods=['POST'])
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

@app.route('/subir-archivo-diccionario', methods=['POST'])
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

if __name__ == '__main__':
    app.run(threaded = True, port = 5000, debug = True)
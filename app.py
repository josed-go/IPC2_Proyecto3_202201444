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

@app.route("/devolverHashtags", methods = ['POST'])
def obtener_hashtags():
    fecha_in = request.form.get('fecha_in')
    fecha_fin = request.form.get('fecha_fin')
    
    respuesta = func.consultar_hashtags(fecha_in, fecha_fin)

    return jsonify({
        'fecha_inicio': fecha_in,
        'fecha_fin': fecha_fin,
        'hashtags': respuesta
    })

@app.route("/devolverMenciones", methods = ['POST'])
def obtener_menciones():

    fecha_in = request.form.get('fecha_in')
    fecha_fin = request.form.get('fecha_fin')
    if fecha_in == None and fecha_fin == None:
        return jsonify({
            'message': 'Debe seleccionar una fecha'
    })
    respuesta = func.consultar_menciones(fecha_in, fecha_fin)

    return jsonify({
        'fecha_inicio': fecha_in,
        'fecha_fin': fecha_fin,
        'menciones': respuesta
    })

@app.route("/limpiarDatos", methods = ['POST'])
def limpiar_datos():
    func.limpiar_datos()

    return jsonify({
        'message': 'Datos limpiados correctamente'
    })

@app.route("/devolverSentimientos", methods = ['GET'])
def obtener_sentimientos():
    fecha_in = request.form.get('fecha_in')
    fecha_fin = request.form.get('fecha_fin')
    respuesta = func.consultar_sentimientos(fecha_in, fecha_fin)

    return jsonify({
        'fecha_inicio': fecha_in,
        'fecha_fin': fecha_fin,
        'respuesta': respuesta
    })

# @app.route("/crearArchivoSalidaMensajes", methods = ['POST'])
# def crear_archivo_mensajes():
#     func.archivo_mensajes_salida()

#     return jsonify({
#         'message': 'Archivo creado con exito'
#     })

if __name__ == '__main__':
    app.run(threaded = True, port = 5000, debug = True)
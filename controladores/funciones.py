import xml.etree.ElementTree as ET
import re
from datetime import datetime

from clases.mensaje import Mensaje


class funciones:
    def __init__(self):
        self.mensajes = []
        self.palabras_positivas = []
        self.palabras_negativas = []

    def cargar_archivo_mensajes(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()

        for mensajes in root.findall('./MENSAJE'):

            fecha = mensajes.find('FECHA')
            texto = mensajes.find('TEXTO')

            # print("Fecha:",self.extraer_fecha(fecha.text)[0])
            nueva_fecha = self.extraer_fecha(fecha.text)[0]

            # print("Hashtags:", self.extraer_hashtags(texto.text))
            hashtags = self.extraer_hashtags(texto.text)

            # print("Usuarios:", self.extrar_usuarios(texto.text))
            usuarios = self.extrar_usuarios(texto.text)

            cantidad_posi, cantidad_nega, tipo = self.calcular_palabras(texto.text)

            # print("Positivas:", cantidad_posi, "Negativas:", cantidad_nega, "Tipo:", tipo)

            # print("Texto:", texto.text)

            nuevo_mensaje = Mensaje(nueva_fecha, texto.text, tipo, cantidad_posi, cantidad_nega, usuarios, hashtags)

            self.mensajes.append(nuevo_mensaje)

        for mensaje in self.mensajes:
            print("Fecha:", mensaje.fecha, "Texto:", mensaje.texto, "Tipo:", mensaje.tipo, "Posi:", mensaje.cantidad_positivas, "Nega:", mensaje.cantidad_negativas, "Usuarios:", mensaje.usuarios, "Hashtags:", mensaje.hashtags)


    def extraer_fecha(self, texto):
        patron = r'\b\d{2}/\d{2}/\d{4}\b'

        return re.findall(patron, texto)
    
    def extraer_hashtags(self, texto):
        # patron = r'(?<=\#)(.*?)(?=\#)'
        # patron = r'(?<=#)([^#]+)(?=#)'
        # patron = r'r#\w+'
        # patron = r'(?<=#)([A-Za-z0-9_]+)(?=#)'
        patron = r'(?<=#)([A-Za-z0-9_À-ÿ]+)(?=#)'

        return re.findall(patron, texto)
    
    def extrar_usuarios(self, texto):
        patron = r'(?<=@)([A-Za-z0-9_À-ÿ]+)'

        return re.findall(patron, texto)
    
    def calcular_palabras(self, texto):
        cantidad_positivas = 0
        cantidad_negativas = 0
        tipo = 'Neutro'

        # PALABRAS POSITIVAS 
        for palabra in self.palabras_positivas:
            if palabra.lower() in texto.lower():
                cantidad_positivas += 1

        # PALABRAS NEGATIVAS
        for palabra in self.palabras_negativas:
            if palabra.lower() in texto.lower():
                cantidad_negativas += 1

        # Tipo

        if cantidad_positivas > cantidad_negativas:
            tipo = 'Positivo'
        elif cantidad_negativas > cantidad_positivas:
            tipo = 'Negativo'

        return cantidad_positivas, cantidad_negativas, tipo


    def cargar_archivo_diccionario(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()

        for positivas in root.findall('./sentimientos_positivos/palabra'):
            self.palabras_positivas.append(positivas.text)

        print(self.palabras_positivas)

        for negativas in root.findall('./sentimientos_negativos/palabra'):
            self.palabras_negativas.append(negativas.text)

        print(self.palabras_negativas)

    def consultar_hashtags(self, fecha_in, fecha_f):
        respuesta = {
            'No hay Hashtags en esta fecha'
        }
        lista_temp = []
        date_format = '%d/%m/%Y'
        fecha_inicio = datetime.strptime(fecha_in, date_format)
        # print(fecha_inicio)
        fecha_fin = datetime.strptime(fecha_f, date_format)
        # print(fecha_fin)
        for mensaje in self.mensajes:
            fecha = datetime.strptime(mensaje.fecha, date_format)
            # print(fecha)
            if (fecha >= fecha_inicio) and (fecha <= fecha_fin):
                # print("hola")
                lista_temp += mensaje.hashtags

        if len(lista_temp) > 0:
            respuesta = {}
            hashtags_unicos = list(set(lista_temp))

            for hashtag in hashtags_unicos:
                respuesta[hashtag] = lista_temp.count(hashtag)

        print(hashtags_unicos)

        return respuesta
        
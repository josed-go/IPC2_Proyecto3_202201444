import xml.etree.ElementTree as ET
import re
from datetime import datetime

from clases.mensaje import Mensaje

import os


class funciones:
    def __init__(self):
        self.mensajes = []
        self.palabras_positivas = []
        self.palabras_negativas = []

        self.palabras_posi_rechazadas = 0
        self.palabras_nega_rechazadas = 0

        self.fechas = []

    def cargar_archivo_mensajes(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()

        for mensajes in root.findall('./MENSAJE'):

            fecha = mensajes.find('FECHA')
            texto = mensajes.find('TEXTO')

            # print("Fecha:",self.extraer_fecha(fecha.text)[0])
            nueva_fecha = self.extraer_fecha(fecha.text)[0]

            if nueva_fecha not in self.fechas:
                self.fechas.append(nueva_fecha)

            # print("Hashtags:", self.extraer_hashtags(texto.text))
            hashtags = self.extraer_hashtags(texto.text)

            # print("Usuarios:", self.extrar_usuarios(texto.text))
            usuarios = self.extrar_usuarios(texto.text)

            cantidad_posi, cantidad_nega, tipo = self.calcular_palabras(texto.text.lower())

            # print("Positivas:", cantidad_posi, "Negativas:", cantidad_nega, "Tipo:", tipo)

            # print("Texto:", texto.text)

            nuevo_mensaje = Mensaje(nueva_fecha, texto.text, tipo, cantidad_posi, cantidad_nega, usuarios, hashtags)

            self.mensajes.append(nuevo_mensaje)

        self.archivo_mensajes_salida()
        self.db_simulada()

        # for mensaje in self.mensajes:
        #     print("Fecha:", mensaje.fecha, "Texto:", mensaje.texto, "Tipo:", mensaje.tipo, "Posi:", mensaje.cantidad_positivas, "Nega:", mensaje.cantidad_negativas, "Usuarios:", mensaje.usuarios, "Hashtags:", mensaje.hashtags)


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
        tipo = ''

        texto = re.sub(r'[.|,|"|;|;|¡|!|?|¿|%|&|$]', "", texto)

        texto_nuevo = texto.split()
        print(texto_nuevo)

        # PALABRAS POSITIVAS 
        for palabra in self.palabras_positivas:
            if palabra.lower() in texto_nuevo:
                print("posi", palabra)
                cantidad_positivas += 1

        # PALABRAS NEGATIVAS
        for palabra in self.palabras_negativas:
            if palabra.lower() in texto_nuevo:
                print("nega", palabra)
                cantidad_negativas += 1

        # Tipo

        if cantidad_positivas > cantidad_negativas:
            tipo = 'Positivo'
        elif cantidad_negativas > cantidad_positivas:
            tipo = 'Negativo'
        elif cantidad_positivas == cantidad_negativas:
            tipo = 'Neutro'

        return cantidad_positivas, cantidad_negativas, tipo


    def cargar_archivo_diccionario(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()

        for positivas in root.findall('./sentimientos_positivos/palabra'):
            if positivas.text not in self.palabras_positivas:
                self.palabras_positivas.append(positivas.text)


        for negativas in root.findall('./sentimientos_negativos/palabra'):
            if negativas.text not in self.palabras_negativas:
                self.palabras_negativas.append(negativas.text)


        self.archivo_palabras_salida()
        print(self.palabras_positivas)
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

        # print(respuesta)

        return respuesta
    
    def consultar_menciones(self, fecha_in, fecha_f):
        respuesta = {
            'No hay menciones en esta fecha'
        }
        lista_temp = []
        date_format = '%d/%m/%Y'
        fecha_inicio = datetime.strptime(fecha_in, date_format)
        fecha_fin = datetime.strptime(fecha_f, date_format)

        for mensaje in self.mensajes:
            fecha = datetime.strptime(mensaje.fecha, date_format)
            if (fecha >= fecha_inicio) and (fecha <= fecha_fin):
                lista_temp += mensaje.usuarios

        if len(lista_temp) > 0:
            respuesta = {}
            menciones_unicas = list(set(lista_temp))

            for mencion in menciones_unicas:
                respuesta[mencion] = lista_temp.count(mencion)
        
        return respuesta
    
    def consultar_sentimientos(self, fecha_in, fecha_f):
        cantidad_posi = 0
        cantidad_nega = 0
        cantidad_neu = 0

        lista_temp = []
        date_format = '%d/%m/%Y'
        fecha_inicio = datetime.strptime(fecha_in, date_format)
        fecha_fin = datetime.strptime(fecha_f, date_format)

        for mensaje in self.mensajes:
            fecha = datetime.strptime(mensaje.fecha, date_format)
            if (fecha >= fecha_inicio) and (fecha <= fecha_fin):
                if mensaje.tipo == 'Positivo':
                    cantidad_posi += 1
                elif mensaje.tipo == 'Negativo':
                    cantidad_nega += 1
                elif mensaje.tipo == 'Neutro':
                    cantidad_neu += 1
        
        respuesta = {
            'Mensajes con sentimientos positivos': cantidad_posi,
            'Mensajes con sentimientos negativos': cantidad_nega,
            'Mensajes nuetros': cantidad_neu
        }
        
        return respuesta

    def archivo_mensajes_salida(self):
        data = ET.Element('MENSAJES_RECIBIDOS')
        # lista_fechas = list(set(self.fechas))

        for fechas in self.fechas:
            cont_msg = 0
            cont_usuarios = 0
            cont_hashtags = 0
            tiempo = ET.SubElement(data, 'TIEMPO')
            fecha = ET.SubElement(tiempo, 'FECHA')
            fecha.text = fechas
            for mensajes in self.mensajes:
                if mensajes.fecha == fechas:
                    cont_msg += 1
                    cont_usuarios += len(mensajes.usuarios)
                    cont_hashtags += len(mensajes.hashtags)

            msg = ET.SubElement(tiempo, 'MSJ_RECIBIDOS')
            msg.text = str(cont_msg)
            usr = ET.SubElement(tiempo, 'USR_MENCIONADOS')
            usr.text = str(cont_usuarios)

            hasht = ET.SubElement(tiempo, 'HASH_INCLUIDOS')
            hasht.text = str(cont_hashtags)

            prueba = ET.tostring(data)
            
        self.prettify_xml(data)
        tree = ET.ElementTree(data)
        tree.write("resumenMensajes.xml",encoding="UTF-8",xml_declaration=True)
    
    def archivo_palabras_salida(self):
        # self.palabras_positivas = list(set(self.palabras_positivas))
        # self.palabras_negativas = list(set(self.palabras_negativas))

        for i, posi in enumerate(self.palabras_positivas):
            for num, nega in enumerate(self.palabras_negativas):
                if posi == nega and i < num:
                    self.palabras_negativas.remove(nega)
                    self.palabras_positivas.remove(posi)
                    self.palabras_posi_rechazadas += 1
                elif posi == nega and i > num:
                    self.palabras_negativas.remove(nega)
                    self.palabras_positivas.remove(posi)
                    self.palabras_nega_rechazadas += 1


        data = ET.Element('CONFIG_RECIBIDA')
        palabras_posi = ET.SubElement(data, 'PALABRAS_POSITIVAS')
        palabras_posi.text = str(len(self.palabras_positivas))

        palabras_posi_rechazadas = ET.SubElement(data, 'PALABRAS POSITIVAS RECHAZADAS')
        palabras_posi_rechazadas.text = str(self.palabras_posi_rechazadas)

        palabras_nega_rechazadas = ET.SubElement(data, 'PALABRAS NEGATIVAS RECHAZADAS')
        palabras_nega_rechazadas.text = str(self.palabras_nega_rechazadas)

        palabras_nega = ET.SubElement(data, 'PALABRAS_NEGATIVAS')
        palabras_nega.text = str(len(self.palabras_negativas))

        prueba = ET.tostring(data)
            
        self.prettify_xml(data)
        tree = ET.ElementTree(data)
        tree.write("resumenConfig.xml",encoding="UTF-8",xml_declaration=True)
    
    def db_simulada(self):
        data = ET.Element('MENSAJES')

        for mensajes in self.mensajes:
            mensaje = ET.SubElement(data, 'MENSAJE')
            fecha = ET.SubElement(mensaje, 'FECHA')
            fecha.text = mensajes.fecha

            texto = ET.SubElement(mensaje, 'TEXTO')
            texto.text = mensajes.texto

            user_mencionados = ET.SubElement(mensaje, 'USUARIOS_MENCIONADOS')

            for usuarios in mensajes.usuarios:
                usuario = ET.SubElement(user_mencionados, 'USUARIO')
                usuario.text = usuarios

            hash_mencionados = ET.SubElement(mensaje, 'HASHTAGS_MENCIONADOS')

            for hashtags in mensajes.hashtags:
                hashtag = ET.SubElement(hash_mencionados, 'HASHTAG')
                hashtag.text = hashtags

            tipo = ET.SubElement(mensaje, 'TIPO_MENSAJE')
            tipo.text = mensajes.tipo

            cantidad_posi = ET.SubElement(mensaje, 'CANT_PALABRAS_POSITIVAS')
            cantidad_posi.text = str(mensajes.cantidad_positivas)

            cantidad_nega = ET.SubElement(mensaje, 'CANT_PALABRAS_NEGATIVAS')
            cantidad_nega.text = str(mensajes.cantidad_negativas)

            prueba = ET.tostring(data)
            
        self.prettify_xml(data)
        tree = ET.ElementTree(data)
        tree.write("db_simulada.xml",encoding="UTF-8",xml_declaration=True)

    def limpiar_datos(self):
        self.mensajes.clear()
        self.palabras_positivas.clear()
        self.palabras_negativas.clear()
        self.palabras_posi_rechazadas = 0
        self.palabras_nega_rechazadas = 0

        self.fechas.clear()
        archivos = ["db_simulada.xml", "resumenConfig.xml", "resumenMensajes.xml"]

        for archivo in archivos:
            if os.path.exists(archivo):
                os.remove(archivo)


        print("Sistema inicializado")




    def prettify_xml(self,element, indent='    '):
        queue = [(0, element)]  # (level, element)
        while queue:
            level, element = queue.pop(0)
            children = [(level + 1, child) for child in list(element)]
            if children:
                element.text = '\n' + indent * (level+1) 
            if queue:
                element.tail = '\n' + indent * queue[0][0]  
            else:
                element.tail = '\n' + indent * (level-1)  
            queue[0:0] = children
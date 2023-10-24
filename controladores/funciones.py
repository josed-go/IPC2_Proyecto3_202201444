import xml.etree.ElementTree as ET


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

            print("FEcha:", fecha.text, "Texto:", texto.text)
        
    def cargar_archivo_diccionario(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()

        for positivas in root.findall('./sentimientos_positivos/palabra'):
            self.palabras_positivas.append(positivas.text)

        print(self.palabras_positivas)

        for negativas in root.findall('./sentimientos_negativos/palabra'):
            self.palabras_negativas.append(negativas.text)

        print(self.palabras_negativas)
class Mensaje:
    def __init__(self, fecha, texto, tipo, cantidad_positivas, cantidad_negativas, usuarios, hashtags):
        self.fecha = fecha
        self.texto = texto
        self.tipo = tipo
        self.cantidad_positivas = cantidad_positivas
        self.cantidad_negativas = cantidad_negativas
        self.usuarios = usuarios
        self.hashtags = hashtags
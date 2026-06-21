# Integrantes: Isabel Villasmil, Daniela Tovar
# Clase que representa un producto dentro de la maquina expendedora

class Producto:
    def __init__(self, codigo_cinco_letras, nombre, precio, mensaje_despedida, codigo_matriz, stock_actual):
        self.codigo_cinco_letras = codigo_cinco_letras
        self.nombre = nombre
        self.precio = precio
        self.mensaje_despedida = mensaje_despedida
        self.codigo_matriz = codigo_matriz
        self.stock_actual = stock_actual

    # Modifica la cantidad disponible del producto
    def actualizar_stock(self, cantidad):
        self.stock_actual = self.stock_actual + cantidad

    def __str__(self):
        texto = self.nombre + " | Precio: " + str(self.precio) + " | Stock: " + str(self.stock_actual)
        return texto


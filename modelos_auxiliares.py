# Integrantes: Isabel Villasmil, Daniela Tovar
# Clases de apoyo para la maquina

class Venta:
    def __init__(self, producto_vendido, total_pagado):
        self.producto_vendido = producto_vendido
        self.total_pagado = total_pagado

    def __str__(self):
        texto = "Venta: " + str(self.producto_vendido) + " | Total: " + str(self.total_pagado)
        return texto


class Restock:
    def __init__(self):
        self.productos_repuestos = []

    # Guarda el registro de cuando llenamos la maquina
    def registrar_reposicion(self, producto, cantidad):
        producto.actualizar_stock(cantidad)
        registro = {"producto": producto.nombre, "cantidad": cantidad}
        self.productos_repuestos.append(registro)

    def __str__(self):
        texto = "Restock realizado: " + str(len(self.productos_repuestos)) + " productos repuestos"
        return texto


class Reporte:
    def __init__(self):
        self.historial_ventas = []

    # Guarda la informacion de compra
    def agregar_venta(self, venta):
        self.historial_ventas.append(venta)

    # Cuenta el numero de transacciones
    def total_ventas(self):
        return len(self.historial_ventas)

    def __str__(self):
        texto = "Reporte con " + str(self.total_ventas()) + " ventas registradas"
        return texto



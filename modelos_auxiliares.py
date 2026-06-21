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


# Pruebas rapidas para verificar que todo funciona
from producto import Producto

p1 = Producto("PEPSI", "Pepsi", 1.25, "Gracias por tu compra!", "B2", 8)

# Probar Venta
v1 = Venta(p1.nombre, p1.precio)
print(v1)

# Probar Reporte
reporte = Reporte()
reporte.agregar_venta(v1)
reporte.agregar_venta(Venta("Doritos", 2.0))
print(reporte)

# Probar Restock
restock = Restock()
print("Stock antes:", p1.stock_actual)
restock.registrar_reposicion(p1, 5)
print("Stock despues de reponer:", p1.stock_actual)
print(restock)

# Integrantes: Isabel Villasmil, Daniela Tovar
# Clases de apoyo para la maquina

class Venta:
    """
    Modela el registro de una venta individual completada exitosamente.
    
    Consideraciones de Eficiencia:
    - O(1) en todos sus métodos. Solo mantiene un registro estático en memoria.
    """
    def __init__(self, producto_vendido, total_pagado, usuario="Anonimo"):
        """
        Guarda los datos esenciales de la transacción comercial.
        
        Eficiencia: O(1). Asignación simple de 3 variables.
        """
        self.producto_vendido = producto_vendido
        self.total_pagado = total_pagado
        self.usuario = usuario

    def __str__(self):
        """
        Genera la representación en formato legible de la venta.
        Eficiencia: O(1).
        """
        texto = "Venta: " + str(self.producto_vendido) + " | Total: " + str(self.total_pagado) + " | Usuario: " + str(self.usuario)
        return texto


class Restock:
    """
    Administra el historial de reposiciones de productos en el inventario.
    
    Consideraciones de Eficiencia:
    - O(1) amortizado para registrar nuevas reposiciones, ya que utiliza
      el método append sobre una lista.
    """
    def __init__(self):
        """
        Prepara la lista donde se guardarán los historiales de reposición.
        Eficiencia: O(1).
        """
        # Lista vacía para acumular el histórico de abastecimiento
        self.productos_repuestos = []

    def registrar_reposicion(self, producto, cantidad):
        """
        Actualiza el stock del producto y anota el evento en el registro.
        
        Eficiencia: 
        - O(1) amortizado, ya que actualizar_stock es O(1) y 
          el append del diccionario a la lista también es O(1) amortizado.
        """
        # Aumentamos la disponibilidad del producto
        producto.actualizar_stock(cantidad)
        
        # Guardamos un diccionario con el detalle de lo que se reabasteció
        registro = {"producto": producto.nombre, "cantidad": cantidad}
        self.productos_repuestos.append(registro)

    def __str__(self):
        """
        Devuelve un resumen textual de los restocks.
        Eficiencia: O(1) porque len() sobre una lista en Python es de tiempo constante.
        """
        texto = "Restock realizado: " + str(len(self.productos_repuestos)) + " productos repuestos"
        return texto


class Reporte:
    """
    Almacena y gestiona el historial general de ventas del sistema.
    
    Consideraciones de Eficiencia:
    - O(1) amortizado para agregar ventas nuevas.
    """
    def __init__(self):
        """
        Inicializa la lista que contendrá todos los objetos de Venta.
        Eficiencia: O(1).
        """
        # El historial recolectará todas las transacciones de compra
        self.historial_ventas = []

    def agregar_venta(self, venta):
        """
        Añade una venta recién completada al historial.
        
        Eficiencia: O(1) amortizado por el uso de append() en la lista.
        """
        self.historial_ventas.append(venta)

    def total_ventas(self):
        """
        Retorna la cantidad de ventas almacenadas.
        
        Eficiencia: O(1). La función len() se ejecuta en tiempo constante.
        """
        return len(self.historial_ventas)

    def __str__(self):
        """
        Devuelve un texto resumen del reporte.
        Eficiencia: O(1).
        """
        texto = "Reporte con " + str(self.total_ventas()) + " ventas registradas"
        return texto

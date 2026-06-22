# Integrantes: Isabel Villasmil, Daniela Tovar
# Clase que representa un producto dentro de la maquina expendedora

class Producto:
    """
    Representa un artículo disponible dentro de la máquina expendedora.
    
    Consideraciones de Eficiencia:
    - La complejidad de la clase en su totalidad es O(1), dado que no
      contiene iteraciones ni estructuras complejas. Solo gestiona estado.
    """
    
    def __init__(self, codigo_cinco_letras, nombre, precio, mensaje_despedida, codigo_matriz, stock_actual):
        """
        Inicializa un nuevo producto con sus atributos básicos.
        
        Eficiencia:
        - O(1): Se realizan únicamente asignaciones en memoria para los atributos.
        """
        # Guardamos la información básica que define a nuestro producto
        self.codigo_cinco_letras = codigo_cinco_letras
        self.nombre = nombre
        self.precio = precio
        self.mensaje_despedida = mensaje_despedida
        self.codigo_matriz = codigo_matriz
        self.stock_actual = stock_actual

    def actualizar_stock(self, cantidad):
        """
        Modifica la cantidad disponible del producto sumando el valor recibido.
        Puede recibir números negativos (ventas) o positivos (restock).
        
        Eficiencia:
        - O(1): Realiza una operación aritmética simple de suma/resta.
        """
        # Se suma la cantidad para actualizar de forma dinámica el inventario
        self.stock_actual = self.stock_actual + cantidad

    def __str__(self):
        """
        Genera una representación en formato texto del producto.
        
        Eficiencia:
        - O(1): Solo se concatenan strings de longitud fija.
        """
        # Formateamos los datos más relevantes para su visualización
        texto = self.nombre + " | Precio: " + str(self.precio) + " | Stock: " + str(self.stock_actual)
        return texto

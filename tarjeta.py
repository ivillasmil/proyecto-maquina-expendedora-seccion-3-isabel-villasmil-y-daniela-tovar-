# Integrantes: Isabel Villasmil, Daniela Tovar
# Clase que representa una tarjeta de pago del cliente

class Tarjeta:
    """
    Representa una tarjeta de pago utilizada por el cliente para las compras.
    
    Consideraciones de Eficiencia:
    - La complejidad de la clase es de O(1), ya que se limita a manipular
      valores numéricos sin utilizar listas o ciclos internos.
    """
    
    def __init__(self, numero_hash, saldo_disponible):
        """
        Inicializa la tarjeta con su identificador y su saldo actual.
        
        Eficiencia:
        - O(1): Únicamente se asignan dos variables en memoria.
        """
        # El numero_hash es una versión segura o codificada del número original
        self.numero_hash = numero_hash
        self.saldo_disponible = saldo_disponible

    def descontar_saldo(self, monto):
        """
        Resta el dinero correspondiente a una compra del saldo de la tarjeta.
        
        Eficiencia:
        - O(1): Es una resta aritmética simple y directa.
        """
        # Actualizamos el saldo restando el costo del producto adquirido
        self.saldo_disponible = self.saldo_disponible - monto

    def __str__(self):
        """
        Retorna la representación en texto de la tarjeta.
        
        Eficiencia:
        - O(1): Concatenación básica de strings.
        """
        # Muestra el número ofuscado y el dinero que le resta a la tarjeta
        texto = "Tarjeta #" + str(self.numero_hash) + " | Saldo: " + str(self.saldo_disponible)
        return texto

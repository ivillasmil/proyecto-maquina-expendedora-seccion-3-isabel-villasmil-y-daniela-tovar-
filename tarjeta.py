# Integrantes: Isabel Villasmil, Daniela Tovar
# Clase que representa una tarjeta de pago del cliente

class Tarjeta:
    def __init__(self, numero_hash, saldo_disponible):
        self.numero_hash = numero_hash
        self.saldo_disponible = saldo_disponible

    # Resta el dinero gastado de la tarjeta
    def descontar_saldo(self, monto):
        self.saldo_disponible = self.saldo_disponible - monto

    def __str__(self):
        texto = "Tarjeta #" + str(self.numero_hash) + " | Saldo: " + str(self.saldo_disponible)
        return texto


# Pruebas rapidas
t1 = Tarjeta(123456789, 50.0)
print(t1)

t1.descontar_saldo(10.5)
print("Saldo despues de pagar 10.5:", t1.saldo_disponible)

t1.descontar_saldo(20.0)
print("Saldo despues de pagar 20.0:", t1.saldo_disponible)

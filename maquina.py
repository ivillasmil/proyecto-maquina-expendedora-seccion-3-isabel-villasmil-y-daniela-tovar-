# Integrantes: Isabel Villasmil, Daniela Tovar
import requests
from producto import Producto
from tarjeta import Tarjeta

class MaquinaExpendedora:
    def __init__(self):
        self.inventario = []
        self.tarjetas_registradas = []
        self.url_productos = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/productos.json"
        self.url_clientes = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/clientes.json"

    def cargar_archivos_iniciales(self):
        print("Cargando base de datos desde GitHub...")
        
        # Intentar cargar los productos
        try:
            respuesta_productos = requests.get(self.url_productos)
            datos_productos = respuesta_productos.json()
            
            # Coordenadas dinamicas
            filas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            columnas = "123456789"
            coordenadas = []
            for f in filas:
                for c in columnas:
                    coordenadas.append(f + c)
            
            indice_matriz = 0
            
            for item in datos_productos:
                # Si hay precio, lo usamos. Si no, ponemos 0.0
                precio_api = item.get("precio", 0.0)
                
                # Asignar un stock base de 10 unidades para empezar
                nuevo_producto = Producto(
                    codigo_cinco_letras=item.get("cod", "XXXXX"),
                    nombre=item.get("prod", "Sin Nombre"),
                    precio=precio_api,
                    mensaje_despedida=item.get("despedida", "Gracias!"),
                    codigo_matriz=coordenadas[indice_matriz],
                    stock_actual=10
                )
                self.inventario.append(nuevo_producto)
                indice_matriz = indice_matriz + 1
                
            print("Se cargaron", len(self.inventario), "productos correctamente.")
            
        except Exception as e:
            print("Error al cargar los productos de la API. Revisa tu conexion o los datos.")
            print("Detalle:", e)

        # Intentar cargar los clientes/tarjetas
        try:
            respuesta_clientes = requests.get(self.url_clientes)
            datos_clientes = respuesta_clientes.json()
            
            for item in datos_clientes:
                nueva_tarjeta = Tarjeta(
                    numero_hash=hash(item.get("id", 0)),
                    saldo_disponible=item.get("saldo", 0.0)
                )
                self.tarjetas_registradas.append(nueva_tarjeta)
                
            print("Se cargaron", len(self.tarjetas_registradas), "tarjetas correctamente.")
            
        except Exception as e:
            print("Error al cargar las tarjetas de la API. Revisa tu conexion.")
            print("Detalle:", e)

# Pruebas de la clase Maquina para el Commit 4
if __name__ == "__main__":
    maquina = MaquinaExpendedora()
    maquina.cargar_archivos_iniciales()
    
    print("\n--- Verificando primer producto ---")
    if len(maquina.inventario) > 0:
        print(maquina.inventario[0])
        print("Coordenada:", maquina.inventario[0].codigo_matriz)
        
    print("\n--- Verificando primera tarjeta ---")
    if len(maquina.tarjetas_registradas) > 0:
        print(maquina.tarjetas_registradas[0])

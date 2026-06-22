# Integrantes: Isabel Villasmil, Daniela Tovar
import requests
import os
from producto import Producto
from tarjeta import Tarjeta
from modelos_auxiliares import Venta, Reporte, Restock

class MaquinaExpendedora:
    def __init__(self):
        self.inventario = []
        self.tarjetas_registradas = []
        self.gestor_reporte = Reporte()
        self.gestor_restock = Restock()
        self.url_productos = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/productos.json"
        self.url_clientes = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/clientes.json"
        self.archivo_inventario = "inventario.txt"

    def guardar_inventario_txt(self):
        # Guardar cambios en el archivo
        try:
            with open(self.archivo_inventario, "w", encoding="utf-8") as archivo:
                for prod in self.inventario:
                    # Formato: coordenada|codigo|nombre|precio|mensaje|stock
                    linea = prod.codigo_matriz + "|" + prod.codigo_cinco_letras + "|" + prod.nombre + "|" + str(prod.precio) + "|" + prod.mensaje_despedida + "|" + str(prod.stock_actual) + "\n"
                    archivo.write(linea)
        except Exception as e:
            print("Error al guardar el inventario local:", e)

    def cargar_archivos_iniciales(self):
        print("Cargando base de datos...")
        
        # 1. Intentar cargar inventario desde archivo local TXT
        if os.path.exists(self.archivo_inventario):
            print("Leyendo estructura fisica desde archivo local inventario.txt...")
            try:
                with open(self.archivo_inventario, "r", encoding="utf-8") as archivo:
                    lineas = archivo.readlines()
                    for linea in lineas:
                        datos = linea.strip().split("|")
                        if len(datos) == 6:
                            prod_cargado = Producto(
                                codigo_matriz=datos[0],
                                codigo_cinco_letras=datos[1],
                                nombre=datos[2],
                                precio=float(datos[3]),
                                mensaje_despedida=datos[4],
                                stock_actual=int(datos[5])
                            )
                            self.inventario.append(prod_cargado)
                print("Se cargaron", len(self.inventario), "productos desde archivo local.")
            except Exception as e:
                print("Error leyendo el TXT local:", e)
        else:
            # 2. Si no existe, cargar desde la API
            print("No se encontro TXT local. Cargando productos desde GitHub...")
            try:
                respuesta_productos = requests.get(self.url_productos)
                datos_productos = respuesta_productos.json()
                
                filas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                columnas = "123456789"
                coordenadas = []
                for f in filas:
                    for c in columnas:
                        coordenadas.append(f + c)
                
                indice_matriz = 0
                for item in datos_productos:
                    precio_api = item.get("precio", 0.0)
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
                print("Se cargaron", len(self.inventario), "productos desde la API.")
                
                # Guardamos inmediatamente para la proxima vez
                self.guardar_inventario_txt()
            except Exception as e:
                print("Error al cargar los productos de la API.")
                print("Detalle:", e)

        # 3. Cargar clientes siempre de la API (asumimos que el saldo es externo)
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
            print("Error al cargar las tarjetas de la API.")
            print("Detalle:", e)

    def mostrar_catalogo_matriz(self):
        print("\n--- Catalogo de Productos ---")
        fila_actual = ""
        linea_imprimir = ""
        
        for producto in self.inventario:
            letra_fila = producto.codigo_matriz[0]
            if fila_actual == "":
                fila_actual = letra_fila
            if letra_fila != fila_actual:
                print(linea_imprimir)
                fila_actual = letra_fila
                linea_imprimir = ""
                
            if producto.stock_actual == 0:
                texto_item = "[  ]"
            else:
                texto_item = "[" + producto.codigo_matriz + "]"
            linea_imprimir = linea_imprimir + texto_item + " "
            
        if linea_imprimir != "":
            print(linea_imprimir)
            
    def procesar_compra(self):
        print("\n--- Comprar Producto ---")
        coord_ingresada = input("Ingrese la coordenada del producto (ej. A1): ")
        
        producto_encontrado = None
        for prod in self.inventario:
            if prod.codigo_matriz == coord_ingresada:
                producto_encontrado = prod
                
        if producto_encontrado == None:
            print("Coordenada no encontrada.")
        elif producto_encontrado.stock_actual <= 0:
            print("El producto no tiene stock.")
        else:
            print("Seleccionado:", producto_encontrado.nombre, "($", producto_encontrado.precio, ")")
            numero_str = input("Ingrese su numero de tarjeta de 18 digitos: ")
            
            try:
                hash_ingresado = hash(int(numero_str))
                
                tarjeta_valida = None
                for tj in self.tarjetas_registradas:
                    if tj.numero_hash == hash_ingresado:
                        tarjeta_valida = tj
                
                if tarjeta_valida == None:
                    print("Tarjeta no registrada o invalida.")
                elif tarjeta_valida.saldo_disponible < producto_encontrado.precio:
                    print("Saldo insuficiente. Tienes $", tarjeta_valida.saldo_disponible)
                else:
                    tarjeta_valida.descontar_saldo(producto_encontrado.precio)
                    producto_encontrado.actualizar_stock(-1)
                    
                    nueva_venta = Venta(producto_encontrado.nombre, producto_encontrado.precio)
                    self.gestor_reporte.agregar_venta(nueva_venta)
                    
                    # Guardar cambios en el archivo: Todo cambio se guarda
                    self.guardar_inventario_txt()
                    
                    print("\n¡Compra exitosa!")
                    print("Nuevo saldo:", tarjeta_valida.saldo_disponible)
                    print(">>", producto_encontrado.mensaje_despedida)
            except ValueError:
                print("Numero de tarjeta invalido, deben ser numeros.")

    def realizar_restock(self):
        print("\n--- Menu de Operario: Restock ---")
        coord_ingresada = input("Ingrese la coordenada del producto a reponer: ")
        
        producto_encontrado = None
        for prod in self.inventario:
            if prod.codigo_matriz == coord_ingresada:
                producto_encontrado = prod
                
        if producto_encontrado == None:
            print("Coordenada no encontrada. Revisa la matriz.")
        else:
            print("Producto seleccionado:", producto_encontrado.nombre, "| Stock actual:", producto_encontrado.stock_actual)
            cant_str = input("Ingrese la cantidad de unidades a agregar: ")
            
            try:
                cantidad = int(cant_str)
                if cantidad > 0:
                    self.gestor_restock.registrar_reposicion(producto_encontrado, cantidad)
                    
                    # Guardar cambios en el archivo: Todo cambio se guarda
                    self.guardar_inventario_txt()
                    print("¡Restock realizado exitosamente! Nuevo stock:", producto_encontrado.stock_actual)
                else:
                    print("La cantidad debe ser mayor a 0.")
            except ValueError:
                print("Cantidad invalida. Debe ser un numero entero.")

    def iniciar_programa(self):
        self.cargar_archivos_iniciales()
        print("\nBienvenido a la Maquina Expendedora!")
        continuar = True
        
        while continuar:
            print("\n--- MENU PRINCIPAL ---")
            print("1. Ver Catalogo (Matriz)")
            print("2. Comprar Producto")
            print("3. Realizar Restock (Operario)")
            print("4. Salir")
            opcion = input("Seleccione una opcion: ")
            
            if opcion == "1":
                self.mostrar_catalogo_matriz()
            elif opcion == "2":
                self.procesar_compra()
            elif opcion == "3":
                self.realizar_restock()
            elif opcion == "4":
                print("Apagando maquina... Hasta luego!")
                continuar = False
            else:
                print("Opcion invalida, intente de nuevo.")

if __name__ == "__main__":
    maquina = MaquinaExpendedora()
    # maquina.iniciar_programa() # Descomentar para probar interactivo

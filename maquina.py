# Integrantes: Isabel Villasmil, Daniela Tovar
import requests
import os
import json
import matplotlib.pyplot as plt
from producto import Producto
from tarjeta import Tarjeta
from modelos_auxiliares import Venta, Reporte, Restock

class MaquinaExpendedora:
    """
    Clase principal que maneja la lógica de la máquina expendedora: inventario,
    ventas, pagos, conexión con API y reportes.
    
    Consideraciones de Eficiencia General:
    - La mayoría de las búsquedas internas iteran sobre el inventario completo,
      resultando en operaciones de orden O(N) donde N es el número de productos.
    """
    def __init__(self):
        """
        Constructor que prepara el entorno y los datos de la máquina.
        
        Eficiencia:
        - O(1): Consta solo de la creación de estructuras vacías y definición
          de cadenas de texto estáticas para rutas y URLs.
        """
        # Se preparan las listas para guardar los datos en memoria durante la ejecución
        self.inventario = []
        self.tarjetas_registradas = []
        
        # Gestores para mantener historiales limpios y ordenados
        self.gestor_reporte = Reporte()
        self.gestor_restock = Restock()
        
        # Enlaces para descargar información externa
        self.url_productos = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/productos.json"
        self.url_clientes = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/clientes.json"
        
        # Definición de ruta estática para no perder datos
        self.archivo_inventario = os.path.join(os.path.dirname(__file__), "inventario.txt")

    def guardar_inventario_txt(self):
        """
        Guarda el inventario actual en el archivo físico.
        
        Eficiencia:
        - O(N) donde N es la cantidad de productos en el inventario. Se itera
          por toda la lista para escribir cada producto en una nueva línea.
        """
        # Utilizamos un bloque try-except para que no colapse si falla el disco
        try:
            with open(self.archivo_inventario, "w", encoding="utf-8") as archivo:
                for prod in self.inventario:
                    # Concatena los datos del producto usando el delimitador |
                    linea = prod.codigo_matriz + "|" + prod.codigo_cinco_letras + "|" + prod.nombre + "|" + str(prod.precio) + "|" + prod.mensaje_despedida + "|" + str(prod.stock_actual) + "\n"
                    archivo.write(linea)
        except Exception as e:
            print("Error al guardar el inventario local:", e)

    def leer_json_local_de_clientes(self):
        """
        Lee la informacion de clientes desde el archivo local clientes.json.
        """
        ruta_clientes = os.path.join(os.path.dirname(__file__), "clientes.json")
        if os.path.exists(ruta_clientes):
            with open(ruta_clientes, "r", encoding="utf-8") as archivo:
                datos_clientes = json.load(archivo)
                for item in datos_clientes:
                    nueva_tarjeta = Tarjeta(
                        numero_hash=hash(item.get("id", 0)),
                        saldo_disponible=item.get("saldo", 0.0)
                    )
                    self.tarjetas_registradas.append(nueva_tarjeta)
        else:
            print("Archivo de clientes locales no encontrado.")

    def cargar_archivos_iniciales(self):
        """
        Lee el archivo de inventario local y consulta las APIs para precios y clientes.
        
        Eficiencia:
        - O(N * M) en la peor de las situaciones, ya que al actualizar los precios,
          itera sobre la lista JSON de la API (M) y, por cada ítem, itera sobre 
          el inventario local (N). Leer los archivos y tarjetas es O(N).
        """
        print("Iniciando sistema...")
        
        # 1. Cargar la lista de productos desde nuestro archivo físico de respaldo
        if os.path.exists(self.archivo_inventario):
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
            # "Si el archivo de productos no se encuentra, debera suponer que la maquina esta vacia"
            print("Archivo de inventario no encontrado. La maquina esta vacia.")

        # 2. Conectándose automáticamente al repositorio para revisar si ha cambiado el precio
        print("Revisando actualizacion de precios en la red...")
        try:
            respuesta_productos = requests.get(self.url_productos)
            datos_productos = respuesta_productos.json()
            
            # Recorrer nuestro inventario local y actualizar precios si coinciden con la API
            for item in datos_productos:
                codigo_api = item.get("cod", "")
                precio_api = item.get("precio", 0.0)
                
                # Búsqueda lineal O(N) para encontrar el producto a actualizar
                for prod in self.inventario:
                    if prod.codigo_cinco_letras == codigo_api:
                        prod.precio = precio_api
            
            print("Precios actualizados exitosamente.")
            self.guardar_inventario_txt() # Guardar cambios en el archivo inmediatamente
        except Exception as e:
            # "Si no se logra conectar al repositorio, debera suponer que los precios no han cambiado"
            print("No se pudo conectar al repositorio. Se mantienen los precios actuales.")

        # 3. Cargar la lista oficial de clientes y sus tarjetas
        try:
            self.leer_json_local_de_clientes()
            print("Se cargaron", len(self.tarjetas_registradas), "tarjetas correctamente.")
        except Exception as e:
            print("Error al cargar las tarjetas locales:", e)

    def mostrar_catalogo_matriz(self):
        """
        Dibuja la matriz visual de los productos en la consola.
        
        Eficiencia:
        - O(Filas * Columnas * N), donde N es la cantidad de productos en el inventario.
          Al buscar en cada posición, realiza un recorrido del inventario (O(N)).
        """
        print("\n  A     B     C     D")
        for fila in range(1, 6):
            linea = f"{fila}"
            for col in ['A', 'B', 'C', 'D']:
                coord = f"{col}{fila}"
                producto_str = "     "
                # Recorre el inventario en cada celda para encontrar la coincidencia
                for prod in self.inventario:
                    if prod.codigo_matriz == coord:
                        producto_str = prod.codigo_cinco_letras[:5].ljust(5)
                linea += f" {producto_str}"
            print(linea)
            
    def procesar_compra(self):
        """
        Coordina la lógica completa para vender un producto y cobrar.
        
        Eficiencia:
        - O(N + M): Requiere recorrer la lista de productos (N) para hallar la 
          coordenada, y luego la lista de tarjetas (M) para validar el pago.
        """
        print("\n--- Comprar Producto ---")
        coord_ingresada = input("Ingrese la coordenada del producto (ej. A1): ")
        
        producto_encontrado = None
        # Búsqueda lineal O(N) para el producto
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
                
                # Búsqueda lineal O(M) para la tarjeta
                for tj in self.tarjetas_registradas:
                    if tj.numero_hash == hash_ingresado:
                        tarjeta_valida = tj
                
                if tarjeta_valida == None:
                    print("Tarjeta no registrada o invalida.")
                elif tarjeta_valida.saldo_disponible < producto_encontrado.precio:
                    print("Saldo insuficiente.")
                else:
                    # Descontamos fondos y restamos del inventario (ambas O(1))
                    tarjeta_valida.descontar_saldo(producto_encontrado.precio)
                    producto_encontrado.actualizar_stock(-1)
                    
                    # Registramos el evento (O(1) amortizado)
                    nueva_venta = Venta(producto_encontrado.nombre, producto_encontrado.precio, tarjeta_valida.numero_hash)
                    self.gestor_reporte.agregar_venta(nueva_venta)
                    
                    # Persistimos la data (O(N))
                    self.guardar_inventario_txt()
                    
                    print("\n¡Compra exitosa!")
                    print(">>", producto_encontrado.mensaje_despedida)
            except ValueError:
                print("Numero de tarjeta invalido.")

    def realizar_restock(self):
        """
        Permite al operador sumar stock a un producto particular.
        
        Eficiencia:
        - O(N): Debido a la necesidad de recorrer la lista de inventario una vez 
          para localizar el producto a reabastecer.
        """
        print("\n--- Menu de Operario: Restock ---")
        coord_ingresada = input("Ingrese la coordenada del producto a reponer: ")
        
        producto_encontrado = None
        # Búsqueda lineal del producto O(N)
        for prod in self.inventario:
            if prod.codigo_matriz == coord_ingresada:
                producto_encontrado = prod
                
        if producto_encontrado == None:
            print("Coordenada no encontrada.")
        else:
            print("Producto seleccionado:", producto_encontrado.nombre, "| Stock actual:", producto_encontrado.stock_actual)
            cant_str = input("Ingrese la cantidad a agregar: ")
            try:
                cantidad = int(cant_str)
                if cantidad > 0:
                    # Actualización de inventario interno O(1)
                    self.gestor_restock.registrar_reposicion(producto_encontrado, cantidad)
                    # Respaldo en texto O(N)
                    self.guardar_inventario_txt()
                    print("¡Restock realizado exitosamente!")
                else:
                    print("La cantidad debe ser mayor a 0.")
            except ValueError:
                print("Cantidad invalida.")

    def generar_reportes(self):
        """
        Crea un resumen de ventas (TXT) y traza gráficos de análisis usando Matplotlib.
        
        Eficiencia:
        - O(V * N): V es la cantidad de ventas en el historial, y N es la cantidad 
          de productos (necesario buscar stocks actuales).
          La graficación toma tiempo constante adicional dependiente de la librería.
        """
        print("\n--- Generando Reportes... ---")
        if len(self.gestor_reporte.historial_ventas) == 0:
            print("No hay ventas registradas para generar reportes.")
            return

        total_vendidos = len(self.gestor_reporte.historial_ventas)
        dinero_cobrado = 0.0
        
        # Diccionarios para agrupar ventas con una eficiencia O(1) en inserción/búsqueda
        dinero_por_usuario = {}
        ventas_por_producto = {}

        # O(V) al iterar todas las ventas
        for v in self.gestor_reporte.historial_ventas:
            dinero_cobrado += v.total_pagado
            
            if v.usuario in dinero_por_usuario:
                dinero_por_usuario[v.usuario] += v.total_pagado
            else:
                dinero_por_usuario[v.usuario] = v.total_pagado
                
            if v.producto_vendido in ventas_por_producto:
                ventas_por_producto[v.producto_vendido] += 1
            else:
                ventas_por_producto[v.producto_vendido] = 1

        # Generar Reporte TXT
        try:
            ruta_txt = os.path.join(os.path.dirname(__file__), "reporte_metricas.txt")
            with open(ruta_txt, "w", encoding="utf-8") as f:
                f.write("--- REPORTE DE VENTAS ---\n")
                f.write("Total de productos vendidos: " + str(total_vendidos) + "\n")
                f.write("Dinero total cobrado: $" + str(round(dinero_cobrado, 2)) + "\n\n")
                f.write("--- DINERO POR USUARIO ---\n")
                # Iterar el diccionario O(U) donde U son los usuarios únicos
                for usr, total in dinero_por_usuario.items():
                    f.write("Usuario ID " + str(usr) + ": $" + str(round(total, 2)) + "\n")
            print("1. Archivo reporte_metricas.txt guardado exitosamente.")
        except Exception as e:
            print("Error al guardar el TXT de metricas:", e)

        # Crear imagenes con los resultados
        try:
            # 1. Grafico comparativo de lo que hay vs lo que se vendio
            plt.figure(figsize=(10, 5))
            nombres_prod = list(ventas_por_producto.keys())
            cant_ventas = list(ventas_por_producto.values())
            
            stocks_actuales = []
            # O(P * N) donde P = prods distintos vendidos y N = inventario total
            for nombre in nombres_prod:
                stock = 0
                for p in self.inventario:
                    if p.nombre == nombre:
                        stock = p.stock_actual
                stocks_actuales.append(stock)
                
            x_pos = range(len(nombres_prod))
            plt.bar(x_pos, cant_ventas, width=0.4, label='Vendidos', align='center')
            plt.bar([p + 0.4 for p in x_pos], stocks_actuales, width=0.4, label='Stock Actual', align='center')
            plt.xticks([p + 0.2 for p in x_pos], nombres_prod, rotation=45, ha="right")
            plt.title("Stock vs Ventas (Productos con movimiento)")
            plt.legend()
            plt.tight_layout()
            ruta_barras = os.path.join(os.path.dirname(__file__), "grafico_barras.png")
            plt.savefig(ruta_barras)
            plt.close()
            print("2. Grafico grafico_barras.png guardado.")

            # 2. Porcentaje de gasto por cliente
            plt.figure()
            etiquetas_usuarios = ["ID "+str(u) for u in dinero_por_usuario.keys()]
            valores_usuarios = list(dinero_por_usuario.values())
            plt.pie(valores_usuarios, labels=etiquetas_usuarios, autopct='%1.1f%%')
            plt.title("Distribucion de Ingresos por Usuario")
            ruta_circular = os.path.join(os.path.dirname(__file__), "grafico_circular.png")
            plt.savefig(ruta_circular)
            plt.close()
            print("3. Grafico grafico_circular.png guardado.")

            # 3. Crecimiento de las ganancias
            plt.figure()
            evolucion = []
            suma_temporal = 0
            # O(V) donde V es el total de ventas
            for v in self.gestor_reporte.historial_ventas:
                suma_temporal += v.total_pagado
                evolucion.append(suma_temporal)
            plt.plot(range(1, len(evolucion) + 1), evolucion, marker='o', linestyle='-')
            plt.title("Crecimiento de Ingresos en el Tiempo")
            plt.xlabel("Numero de Venta")
            plt.ylabel("Ingreso Acumulado ($)")
            plt.xticks(range(1, len(evolucion) + 1))
            plt.grid(True)
            ruta_lineas = os.path.join(os.path.dirname(__file__), "grafico_lineas.png")
            plt.savefig(ruta_lineas)
            plt.close()
            print("4. Grafico grafico_lineas.png guardado.")
            
        except Exception as e:
            print("Error al generar los graficos de Matplotlib:", e)

    def iniciar_programa(self):
        """
        Inicia el ciclo principal (loop infinito controlado) de interacción.
        
        Eficiencia:
        - O(Infinito), ya que es un ciclo 'while' permanente hasta que el usuario
          ordena su fin. El interior del ciclo ejecuta diversas funciones de las 
          cuales la peor es mostrar_catalogo_matriz que es O(N).
        """
        # Ejecuta tareas previas al arranque como conexión y archivos O(N*M)
        self.cargar_archivos_iniciales()
        continuar = True
        
        while continuar:
            # Imprime el mapa de productos O(N)
            self.mostrar_catalogo_matriz()
            
            print("\nOpciones: [vacio] = Vender | RS = Restock | RP = Reportes | SALIR = Apagar")
            entrada = input("Introduce el codigo de un producto, o elige una accion: ")
            
            if entrada == "":
                self.procesar_compra()
            elif entrada.upper() == "RS":
                self.realizar_restock()
            elif entrada.upper() == "RP":
                self.generar_reportes()
            elif entrada.upper() == "SALIR":
                print("Apagando maquina... Hasta luego!")
                continuar = False
            else:
                # Si introduce el código de un producto, se le muestra su precio
                # Requiere una iteración lineal O(N)
                producto_buscado = None
                for prod in self.inventario:
                    if prod.codigo_cinco_letras.upper() == entrada.upper() or prod.codigo_matriz.upper() == entrada.upper():
                        producto_buscado = prod
                
                if producto_buscado != None:
                    print("\n>> El precio de", producto_buscado.nombre, "es: $", producto_buscado.precio)
                else:
                    print("\n>> Codigo no reconocido.")

if __name__ == "__main__":
    maquina = MaquinaExpendedora()
    # maquina.iniciar_programa()

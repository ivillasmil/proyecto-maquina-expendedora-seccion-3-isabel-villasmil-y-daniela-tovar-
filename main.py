# ==============================================================================
# Integrantes: Isabel Villasmil, Daniela Tovar
# Proyecto: Maquina Expendedora Inteligente
# Archivo principal para arrancar
# ==============================================================================

from maquina import MaquinaExpendedora

def main():
    """
    Función principal que instancia y enciende la máquina expendedora.
    Maneja las interrupciones para asegurar un apagado controlado.
    
    Consideraciones de Eficiencia:
    - O(1) de forma directa en este bloque, ya que solo crea una instancia
      y llama al método principal de la clase. La complejidad real
      dependerá del ciclo de vida dentro de 'app.iniciar_programa()'.
    """
    print("=" * 50)
    print("     Máquina Expendedora     ")
    print("=" * 50)
    
    try:
        # Creamos la instancia de la máquina
        app = MaquinaExpendedora()
        # Arrancamos el ciclo de vida principal del sistema
        app.iniciar_programa()
        
    except KeyboardInterrupt:
        # Capturamos CTRL+C para evitar que el programa colapse abruptamente
        print("\n\nApagado de emergencia activado. ¡Hasta luego!")
    except Exception as e:
        # Capturamos cualquier otro error crítico que pueda ocurrir durante la ejecución
        print(f"\n[ERROR CRITICO] El sistema se ha detenido: {e}")

if __name__ == "__main__":
    main()

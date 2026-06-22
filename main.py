# Integrantes: Isabel Villasmil, Daniela Tovar
# Programa principal de la maquina expendedora (Version con Persistencia)
from maquina import MaquinaExpendedora

def main():
    print("Iniciando sistema de la maquina...")
    m = MaquinaExpendedora()
    m.iniciar_programa()

if __name__ == "__main__":
    main()

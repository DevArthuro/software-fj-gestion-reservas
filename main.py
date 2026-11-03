"""Punto de entrada del programa. Se ejecuta con: python main.py"""

from src.gestor import Gestor  # Clase que guarda las listas del sistema
from src.interfaz.ventana_principal import iniciar_aplicacion  # Función que abre la ventana
from src.logger import registrar_error, registrar_evento  # Funciones del log


def main():
    """Crea el gestor e inicia la aplicación gráfica."""
    try:  # Intenta iniciar el programa
        gestor = Gestor()  # Crea el gestor con las listas vacías
        iniciar_aplicacion(gestor)  # Abre la ventana principal
    except Exception as error:  # Si ocurre cualquier error inesperado
        registrar_error(f"Error inesperado al iniciar: {error}")  # Lo guarda en el log
        print("Ocurrió un problema al iniciar el programa. Revisa el archivo logs/sistema.log.")  # Mensaje amable
    finally:  # Esto se ejecuta siempre, haya error o no
        registrar_evento("Fin de la ejecución del programa.")  # Deja constancia del fin


if __name__ == "__main__":  # Solo se ejecuta si se corre este archivo directamente
    main()  # Llama a la función principal

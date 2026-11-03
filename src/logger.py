"""Registro de eventos y errores en el archivo logs/sistema.log."""

import os  # Permite trabajar con carpetas y rutas de archivos
from datetime import datetime  # Permite obtener la fecha y hora actual

CARPETA_LOGS = "logs"  # Nombre de la carpeta donde se guarda el log
RUTA_LOG = os.path.join(CARPETA_LOGS, "sistema.log")  # Ruta completa del archivo de log


def _escribir(tipo, mensaje):
    """Escribe una línea en el log con fecha, tipo y mensaje."""
    try:  # Intenta escribir; si falla, el programa no se detiene
        os.makedirs(CARPETA_LOGS, exist_ok=True)  # Crea la carpeta si no existe
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual como texto
        linea = f"[{fecha}] [{tipo}] {mensaje}"  # Arma la línea con el formato del log
        with open(RUTA_LOG, "a", encoding="utf-8") as archivo:  # Abre el archivo en modo agregar
            archivo.write(linea + "\n")  # Escribe la línea con salto de línea
    except OSError as error:  # Si hubo un problema con el archivo
        print(f"No se pudo escribir en el log: {error}")  # Avisa por consola sin detener el programa


def registrar_evento(mensaje):
    """Registra un evento normal del sistema."""
    _escribir("EVENTO", mensaje)  # Escribe la línea con el tipo EVENTO


def registrar_error(mensaje):
    """Registra un error del sistema."""
    _escribir("ERROR", mensaje)  # Escribe la línea con el tipo ERROR


def leer_log():
    """Retorna todo el contenido del log como texto."""
    try:  # Intenta abrir el archivo
        with open(RUTA_LOG, "r", encoding="utf-8") as archivo:  # Abre el archivo en modo lectura
            return archivo.read()  # Retorna todo el contenido
    except FileNotFoundError:  # Si el archivo todavía no existe
        return "El archivo de log aún no existe."  # Retorna un mensaje informativo

# ==========================================================
# Archivo: src/interfaz/pestana_logs.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 5
#
# TODO: Text con scroll que muestra leer_log(), botones Actualizar, Limpiar vista y Ejecutar simulación.
#
# IMPORTANTE: el nombre de la función crear_pestana_logs y sus parámetros
# (contenedor, gestor) NO se pueden cambiar, porque la ventana principal
# la llama exactamente así.
# ==========================================================

from tkinter import ttk  # Importa los widgets con estilo de Tkinter


def crear_pestana_logs(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Logs. La completa el Estudiante 5."""
    marco = ttk.Frame(contenedor, padding=20)  # Crea el marco de la pestaña con margen interno
    etiqueta = ttk.Label(marco, text="Pestaña Logs – en construcción (Estudiante 5)")  # Texto temporal
    etiqueta.pack(pady=20)  # Ubica la etiqueta en el marco con espacio vertical
    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

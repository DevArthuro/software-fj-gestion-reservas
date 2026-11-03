# ==========================================================
# Archivo: src/interfaz/pestana_reservas.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 4
#
# TODO: Combobox de cliente y servicio, campo de duración, botones Crear/Confirmar/Cancelar/Procesar, Treeview con estado y costo.
#
# IMPORTANTE: el nombre de la función crear_pestana_reservas y sus parámetros
# (contenedor, gestor) NO se pueden cambiar, porque la ventana principal
# la llama exactamente así.
# ==========================================================

from tkinter import ttk  # Importa los widgets con estilo de Tkinter


def crear_pestana_reservas(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Reservas. La completa el Estudiante 4."""
    marco = ttk.Frame(contenedor, padding=20)  # Crea el marco de la pestaña con margen interno
    etiqueta = ttk.Label(marco, text="Pestaña Reservas – en construcción (Estudiante 4)")  # Texto temporal
    etiqueta.pack(pady=20)  # Ubica la etiqueta en el marco con espacio vertical
    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

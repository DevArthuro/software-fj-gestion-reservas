# ==========================================================
# Archivo: src/interfaz/pestana_servicios.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 3
#
# TODO: Combobox de tipo de servicio, campos según el tipo, botón Crear servicio, Treeview, calculadora de costo con impuesto y descuento.
#
# IMPORTANTE: el nombre de la función crear_pestana_servicios y sus parámetros
# (contenedor, gestor) NO se pueden cambiar, porque la ventana principal
# la llama exactamente así.
# ==========================================================

from tkinter import ttk  # Importa los widgets con estilo de Tkinter


def crear_pestana_servicios(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Servicios. La completa el Estudiante 3."""
    marco = ttk.Frame(contenedor, padding=20)  # Crea el marco de la pestaña con margen interno
    etiqueta = ttk.Label(marco, text="Pestaña Servicios – en construcción (Estudiante 3)")  # Texto temporal
    etiqueta.pack(pady=20)  # Ubica la etiqueta en el marco con espacio vertical
    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

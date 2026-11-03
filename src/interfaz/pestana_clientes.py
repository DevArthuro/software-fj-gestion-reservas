# ==========================================================
# Archivo: src/interfaz/pestana_clientes.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 2
#
# TODO: Formulario con Entry, botón Registrar, Treeview con clientes, botón Eliminar, errores con mostrar_error().
#
# IMPORTANTE: el nombre de la función crear_pestana_clientes y sus parámetros
# (contenedor, gestor) NO se pueden cambiar, porque la ventana principal
# la llama exactamente así.
# ==========================================================

from tkinter import ttk  # Importa los widgets con estilo de Tkinter


def crear_pestana_clientes(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Clientes. La completa el Estudiante 2."""
    marco = ttk.Frame(contenedor, padding=20)  # Crea el marco de la pestaña con margen interno
    etiqueta = ttk.Label(marco, text="Pestaña Clientes – en construcción (Estudiante 2)")  # Texto temporal
    etiqueta.pack(pady=20)  # Ubica la etiqueta en el marco con espacio vertical
    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

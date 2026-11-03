"""Funciones de apoyo para mostrar mensajes en la interfaz."""

from tkinter import messagebox  # Ventanas emergentes de Tkinter

from src.logger import registrar_error, registrar_evento  # Funciones para escribir en el log


def mostrar_error(error):
    """Registra el error en el log y lo muestra en una ventana."""
    texto = str(error)  # Convierte el error a texto
    registrar_error(f"{type(error).__name__}: {texto}")  # Lo registra con el nombre de su clase
    messagebox.showerror("Error", texto)  # Muestra la ventana de error


def mostrar_info(mensaje):
    """Registra el mensaje en el log y lo muestra en una ventana."""
    registrar_evento(mensaje)  # Lo registra como evento
    messagebox.showinfo("Información", mensaje)  # Muestra la ventana de información

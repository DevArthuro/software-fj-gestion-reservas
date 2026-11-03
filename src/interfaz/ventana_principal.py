"""Ventana principal de la aplicación, con pestañas."""

import tkinter as tk  # Librería gráfica
from tkinter import ttk  # Widgets con estilo (Label, Notebook)

from src.interfaz.pestana_clientes import crear_pestana_clientes  # Pestaña de clientes
from src.interfaz.pestana_servicios import crear_pestana_servicios  # Pestaña de servicios
from src.interfaz.pestana_reservas import crear_pestana_reservas  # Pestaña de reservas
from src.interfaz.pestana_logs import crear_pestana_logs  # Pestaña de logs
from src.logger import registrar_evento  # Para registrar inicio y cierre


def iniciar_aplicacion(gestor):
    """Crea la ventana con sus 4 pestañas y la deja abierta hasta que se cierre."""
    ventana = tk.Tk()  # Crea la ventana principal
    ventana.title("Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas")  # Título de la ventana
    ventana.geometry("900x600")  # Tamaño de la ventana

    titulo = ttk.Label(ventana, text="Software FJ", font=("Arial", 16, "bold"))  # Título visible arriba
    titulo.pack(pady=10)  # Lo ubica con espacio vertical

    cuaderno = ttk.Notebook(ventana)  # Contenedor de pestañas
    cuaderno.pack(fill="both", expand=True, padx=10, pady=10)  # Ocupa todo el espacio con margen

    cuaderno.add(crear_pestana_clientes(cuaderno, gestor), text="Clientes")  # Agrega la pestaña Clientes
    cuaderno.add(crear_pestana_servicios(cuaderno, gestor), text="Servicios")  # Agrega la pestaña Servicios
    cuaderno.add(crear_pestana_reservas(cuaderno, gestor), text="Reservas")  # Agrega la pestaña Reservas
    cuaderno.add(crear_pestana_logs(cuaderno, gestor), text="Logs")  # Agrega la pestaña Logs

    registrar_evento("Aplicación gráfica iniciada.")  # Deja constancia de que abrió
    ventana.mainloop()  # Mantiene la ventana abierta hasta que el usuario la cierre
    registrar_evento("Aplicación gráfica cerrada.")  # Deja constancia de que cerró

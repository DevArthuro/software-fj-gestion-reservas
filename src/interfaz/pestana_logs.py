"""
Archivo: src/interfaz/pestana_logs.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 5

Permite consultar los registros y ejecutar la simulación.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from src.logger import leer_log
from simulacion import ejecutar_simulacion


def crear_pestana_logs(contenedor, gestor):
    """Crea la pestaña de registros y simulación."""

    marco = ttk.Frame(contenedor, padding=15)

    titulo = ttk.Label(
        marco,
        text="Registro de eventos y simulación",
        font=("Arial", 14, "bold")
    )
    titulo.pack(pady=10)

    texto_logs = ScrolledText(
        marco,
        width=100,
        height=22,
        wrap=tk.WORD,
        font=("Consolas", 9)
    )
    texto_logs.pack(fill="both", expand=True, pady=10)

    def actualizar_logs():
        """Actualiza el contenido mostrado en pantalla."""

        texto_logs.config(state=tk.NORMAL)
        texto_logs.delete("1.0", tk.END)
        texto_logs.insert(tk.END, leer_log())
        texto_logs.see(tk.END)
        texto_logs.config(state=tk.DISABLED)

    def limpiar_vista():
        """Limpia únicamente el contenido visual."""

        texto_logs.config(state=tk.NORMAL)
        texto_logs.delete("1.0", tk.END)
        texto_logs.config(state=tk.DISABLED)

    def ejecutar_pruebas():
        """Ejecuta la simulación y actualiza los registros."""

        try:
            ejecutar_simulacion()
            actualizar_logs()

            messagebox.showinfo(
                "Simulación finalizada",
                "La simulación terminó. Consulta los resultados en los logs."
            )

        except Exception as error:
            messagebox.showerror(
                "Error en la simulación",
                f"No fue posible ejecutar la simulación:\n{error}"
            )
            actualizar_logs()

    botones = ttk.Frame(marco)
    botones.pack(pady=10)

    ttk.Button(
        botones,
        text="Actualizar",
        command=actualizar_logs
    ).pack(side=tk.LEFT, padx=5)

    ttk.Button(
        botones,
        text="Limpiar vista",
        command=limpiar_vista
    ).pack(side=tk.LEFT, padx=5)

    ttk.Button(
        botones,
        text="Ejecutar simulación",
        command=ejecutar_pruebas
    ).pack(side=tk.LEFT, padx=5)

    actualizar_logs()

    return marco
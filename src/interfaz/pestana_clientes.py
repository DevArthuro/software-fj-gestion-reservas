"""
Archivo: src/interfaz/pestana_clientes.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 2

Interfaz gráfica para registrar, consultar y eliminar clientes.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.cliente import Cliente
from src.excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError
)
from src.logger import registrar_evento, registrar_error


def mostrar_error(mensaje):
    """Muestra los errores en una ventana de diálogo."""

    messagebox.showerror(
        "Error - Software FJ",
        str(mensaje)
    )


def crear_pestana_clientes(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Clientes."""

    marco = ttk.Frame(contenedor, padding=20)

    # ======================================================
    # TÍTULO
    # ======================================================

    titulo = ttk.Label(
        marco,
        text="GESTIÓN DE CLIENTES",
        font=("Arial", 16, "bold")
    )
    titulo.pack(pady=(0, 15))

    # ======================================================
    # FORMULARIO
    # ======================================================

    formulario = ttk.LabelFrame(
        marco,
        text="Datos del cliente",
        padding=15
    )
    formulario.pack(fill="x", pady=10)

    ttk.Label(formulario, text="Nombre").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    entrada_nombre = ttk.Entry(formulario, width=35)
    entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(formulario, text="Documento:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    entrada_documento = ttk.Entry(formulario, width=35)
    entrada_documento.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(formulario, text="Correo").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    entrada_correo = ttk.Entry(formulario, width=35)
    entrada_correo.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(formulario, text="Teléfono").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    entrada_telefono = ttk.Entry(formulario, width=35)
    entrada_telefono.grid(row=3, column=1, padx=5, pady=5)

    # ======================================================
    # TABLA
    # ======================================================

    contenedor_tabla = ttk.LabelFrame(
        marco,
        text="Clientes registrados",
        padding=10
    )
    contenedor_tabla.pack(fill="both", expand=True, pady=10)

    columnas = (
        "id",
        "nombre",
        "documento",
        "correo",
        "telefono"
    )

    tabla = ttk.Treeview(
        contenedor_tabla,
        columns=columnas,
        show="headings",
        height=10
    )

    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("documento", text="Documento")
    tabla.heading("correo", text="Correo")
    tabla.heading("telefono", text="Teléfono")

    tabla.column("id", width=75, anchor="center")
    tabla.column("nombre", width=150)
    tabla.column("documento", width=110, anchor="center")
    tabla.column("correo", width=180)
    tabla.column("telefono", width=110, anchor="center")

    barra_vertical = ttk.Scrollbar(
        contenedor_tabla,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(yscrollcommand=barra_vertical.set)

    tabla.pack(side="left", fill="both", expand=True)
    barra_vertical.pack(side="right", fill="y")

    # ======================================================
    # ACTUALIZAR TABLA
    # ======================================================

    def actualizar_tabla():
        """Actualiza la tabla con los clientes del gestor."""

        for elemento in tabla.get_children():
            tabla.delete(elemento)

        for cliente in gestor.listar_clientes():
            tabla.insert(
                "",
                "end",
                iid=str(cliente.id),
                values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.documento,
                    cliente.correo,
                    cliente.telefono
                )
            )

    # ======================================================
    # GENERAR IDENTIFICADOR
    # ======================================================

    def generar_id():
        """Genera un identificador de cliente no repetido."""

        ids_existentes = {
            str(cliente.id) for cliente in gestor.clientes
        }

        numero = 1

        while f"C{numero:03d}" in ids_existentes:
            numero += 1

        return f"C{numero:03d}"

    # ======================================================
    # REGISTRAR CLIENTE
    # ======================================================

    def registrar_cliente_interfaz():
        """Recoge, valida y registra los datos del formulario."""

        try:
            nombre = entrada_nombre.get().strip()
            documento = entrada_documento.get().strip()
            correo = entrada_correo.get().strip()
            telefono = entrada_telefono.get().strip()

            if not nombre or not documento or not correo or not telefono:
                raise ParametroFaltanteError(
                    "Todos los campos son obligatorios."
                )

            nuevo_cliente = Cliente(
                generar_id(),
                nombre,
                documento,
                correo,
                telefono
            )

            gestor.registrar_cliente(nuevo_cliente)
            actualizar_tabla()

            entrada_nombre.delete(0, tk.END)
            entrada_documento.delete(0, tk.END)
            entrada_correo.delete(0, tk.END)
            entrada_telefono.delete(0, tk.END)

            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente."
            )

        except (ParametroFaltanteError, ClienteInvalidoError) as error:
            registrar_error(
                f"Error en formulario de clientes: {error}"
            )
            mostrar_error(error)

        except Exception as error:
            registrar_error(
                f"Error inesperado en la interfaz de clientes: {error}"
            )
            mostrar_error(
                f"No fue posible registrar el cliente. Detalle: {error}"
            )

    # ======================================================
    # ELIMINAR CLIENTE
    # ======================================================

    def eliminar_cliente_interfaz():
        """Elimina el cliente seleccionado en la tabla."""

        try:
            seleccion = tabla.selection()

            if not seleccion:
                raise ParametroFaltanteError(
                    "Seleccione un cliente de la tabla para eliminarlo."
                )

            valores = tabla.item(seleccion[0], "values")
            documento = valores[2]
            nombre = valores[1]

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Desea eliminar al cliente {nombre}?"
            )

            if confirmar:
                gestor.eliminar_cliente(documento)
                actualizar_tabla()

                messagebox.showinfo(
                    "Eliminación exitosa",
                    "El cliente fue eliminado correctamente."
                )

        except (ParametroFaltanteError, ClienteInvalidoError) as error:
            registrar_error(
                f"Error al eliminar cliente desde la interfaz: {error}"
            )
            mostrar_error(error)

        except Exception as error:
            registrar_error(
                f"Error inesperado al eliminar cliente: {error}"
            )
            mostrar_error(
                f"No fue posible eliminar el cliente. Detalle: {error}"
            )

    # ======================================================
    # BOTONES
    # ======================================================

    botones = ttk.Frame(marco)
    botones.pack(pady=10)

    boton_registrar = ttk.Button(
        botones,
        text="Registrar cliente",
        command=registrar_cliente_interfaz
    )
    boton_registrar.pack(side="left", padx=5)

    boton_eliminar = ttk.Button(
        botones,
        text="Eliminar seleccionado",
        command=eliminar_cliente_interfaz
    )
    boton_eliminar.pack(side="left", padx=5)

    boton_actualizar = ttk.Button(
        botones,
        text="Actualizar tabla",
        command=actualizar_tabla
    )
    boton_actualizar.pack(side="left", padx=5)

    # ======================================================
    # CARGA INICIAL
    # ======================================================

    try:
        actualizar_tabla()
    except Exception as error:
        registrar_error(
            f"Error al cargar la pestaña de clientes: {error}"
        )
        mostrar_error(
            f"No fue posible cargar los clientes: {error}"
        )

    registrar_evento("Pestaña de clientes creada correctamente.")

    return marco
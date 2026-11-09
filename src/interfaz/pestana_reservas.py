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
import tkinter as tk
from tkinter import messagebox

from src.reserva import Reserva
from src.excepciones import (
    ReservaInvalidaError,
    ParametroFaltanteError,
    ServicioNoDisponibleError
)

def crear_pestana_reservas(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Reservas. La completa el Estudiante 4."""
    marco = ttk.Frame(contenedor, padding=20)  # Crea el marco de la pestaña con margen interno
    
    # Formulario para registrar reservas
    formulario = ttk.LabelFrame(
        marco,
        text="Registrar reserva",
        padding=15
    )
    formulario.pack(fill="x", pady=(0, 15))

    ttk.Label(
        formulario,
        text="Cliente:"
    ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

    combo_cliente = ttk.Combobox(
        formulario,
        state="readonly",
        width=35
    )
    combo_cliente.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(
        formulario,
        text="Servicio:"
    ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

    combo_servicio = ttk.Combobox(
        formulario,
        state="readonly",
        width=35
    )
    combo_servicio.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(
        formulario,
        text="Duración (horas):"
    ).grid(row=2, column=0, padx=5, pady=5, sticky="w")

    entrada_duracion = ttk.Entry(formulario, width=38)
    entrada_duracion.grid(row=2, column=1, padx=5, pady=5)

    # Contenedor de botones para gestionar reservas
    contenedor_botones = ttk.Frame(marco)
    contenedor_botones.pack(fill="x", pady=(0, 15))

    boton_crear = ttk.Button(
        contenedor_botones,
        text="Crear reserva"
    )
    boton_crear.pack(side="left", padx=5)

    boton_confirmar = ttk.Button(
        contenedor_botones,
        text="Confirmar"
    )
    boton_confirmar.pack(side="left", padx=5)

    boton_cancelar = ttk.Button(
        contenedor_botones,
        text="Cancelar"
    )
    boton_cancelar.pack(side="left", padx=5)

    boton_procesar = ttk.Button(
        contenedor_botones,
        text="Procesar"
    )
    boton_procesar.pack(side="left", padx=5)

    # Tabla para mostrar las reservas registradas
    contenedor_tabla = ttk.LabelFrame(
        marco,
        text="Reservas registradas",
        padding=10
    )
    contenedor_tabla.pack(fill="both", expand=True, pady=10)

    columnas = (
        "id",
        "cliente",
        "servicio",
        "duracion",
        "estado",
        "costo"
    )

    tabla_reservas = ttk.Treeview(
        contenedor_tabla,
        columns=columnas,
        show="headings",
        height=10
    )

    encabezados = {
        "id": "ID",
        "cliente": "Cliente",
        "servicio": "Servicio",
        "duracion": "Duración (h)",
        "estado": "Estado",
        "costo": "Costo"
    }

    for columna, titulo in encabezados.items():
        tabla_reservas.heading(columna, text=titulo)
        tabla_reservas.column(columna, width=120, anchor="center")

    tabla_reservas.pack(fill="both", expand=True)

    # Cargar clientes y servicios registrados
    clientes_disponibles = []
    servicios_disponibles = []

    def actualizar_opciones():
        """Actualiza los clientes y servicios de los desplegables."""

        clientes_disponibles.clear()
        clientes_disponibles.extend(gestor.listar_clientes())

        servicios_disponibles.clear()
        servicios_disponibles.extend(gestor.listar_servicios())

        combo_cliente["values"] = [
            f"{cliente.nombre} - {cliente.documento}"
            for cliente in clientes_disponibles
        ]

        combo_servicio["values"] = [
            f"{servicio.nombre} - ${servicio.precio_base:,.0f}"
            for servicio in servicios_disponibles
        ]

        combo_cliente.set("")
        combo_servicio.set("")

    boton_actualizar = ttk.Button(
        formulario,
        text="Actualizar clientes y servicios",
        command=actualizar_opciones
    )
    boton_actualizar.grid(
        row=3,
        column=0,
        columnspan=2,
        pady=10
    )

    actualizar_opciones()

    # Crear una reserva desde el formulario
    def crear_reserva():
        """Registra una nueva reserva con los datos seleccionados."""

        try:
            indice_cliente = combo_cliente.current()
            indice_servicio = combo_servicio.current()

            if indice_cliente < 0:
                raise ParametroFaltanteError(
                    "Debe seleccionar un cliente."
                )

            if indice_servicio < 0:
                raise ParametroFaltanteError(
                    "Debe seleccionar un servicio."
                )

            duracion = float(entrada_duracion.get().strip())

            cliente = clientes_disponibles[indice_cliente]
            servicio = servicios_disponibles[indice_servicio]

            id_reserva = f"R{len(gestor.reservas) + 1:03d}"

            reserva = Reserva(
                id_reserva,
                cliente,
                servicio,
                duracion
            )

            gestor.crear_reserva(reserva)

            tabla_reservas.insert(
                "",
                "end",
                iid=reserva.id,
                values=(
                    reserva.id,
                    cliente.nombre,
                    servicio.nombre,
                    reserva.duracion,
                    reserva.estado,
                    f"${reserva.costo:,.2f}"
                )
            )

            entrada_duracion.delete(0, tk.END)

            messagebox.showinfo(
                "Reserva creada",
                "La reserva se registró correctamente."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "La duración debe ser un número válido."
            )

        except (
            ReservaInvalidaError,
            ParametroFaltanteError,
            ServicioNoDisponibleError
        ) as error:
            messagebox.showerror("Error", str(error))

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    boton_crear.config(command=crear_reserva)

    # Confirmar una reserva seleccionada
    def confirmar_reserva():
        """Confirma la reserva seleccionada en la tabla."""

        seleccion = tabla_reservas.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccionar reserva",
                "Debe seleccionar una reserva de la tabla."
            )
            return

        try:
            id_reserva = seleccion[0]

            reserva = next(
                (
                    reserva
                    for reserva in gestor.listar_reservas()
                    if reserva.id == id_reserva
                ),
                None
            )

            if reserva is None:
                raise ReservaInvalidaError(
                    "No se encontró la reserva seleccionada."
                )

            reserva.confirmar()

            tabla_reservas.set(
                id_reserva,
                "estado",
                reserva.estado
            )

            messagebox.showinfo(
                "Reserva confirmada",
                "La reserva se confirmó correctamente."
            )

        except (
            ReservaInvalidaError,
            ParametroFaltanteError,
            ServicioNoDisponibleError
        ) as error:
            messagebox.showerror("Error", str(error))

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    boton_confirmar.config(command=confirmar_reserva)

    # Cancelar una reserva seleccionada
    def cancelar_reserva():
        """Cancela la reserva seleccionada en la tabla."""

        seleccion = tabla_reservas.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccionar reserva",
                "Debe seleccionar una reserva de la tabla."
            )
            return

        try:
            id_reserva = seleccion[0]

            reserva = next(
                (
                    reserva
                    for reserva in gestor.listar_reservas()
                    if reserva.id == id_reserva
                ),
                None
            )

            if reserva is None:
                raise ReservaInvalidaError(
                    "No se encontró la reserva seleccionada."
                )

            reserva.cancelar()

            tabla_reservas.set(
                id_reserva,
                "estado",
                reserva.estado
            )

            messagebox.showinfo(
                "Reserva cancelada",
                "La reserva se canceló correctamente."
            )

        except (
            ReservaInvalidaError,
            ParametroFaltanteError,
            ServicioNoDisponibleError
        ) as error:
            messagebox.showerror("Error", str(error))

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    boton_cancelar.config(command=cancelar_reserva)

    # Procesar una reserva seleccionada
    def procesar_reserva():
        """Calcula el costo de la reserva seleccionada."""

        seleccion = tabla_reservas.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccionar reserva",
                "Debe seleccionar una reserva de la tabla."
            )
            return

        try:
            id_reserva = seleccion[0]

            reserva = next(
                (
                    reserva
                    for reserva in gestor.listar_reservas()
                    if reserva.id == id_reserva
                ),
                None
            )

            if reserva is None:
                raise ReservaInvalidaError(
                    "No se encontró la reserva seleccionada."
                )

            costo = reserva.procesar()

            tabla_reservas.set(
                id_reserva,
                "costo",
                f"${costo:,.2f}"
            )

            messagebox.showinfo(
                "Reserva procesada",
                f"El costo de la reserva es ${costo:,.2f}"
            )

        except (
            ReservaInvalidaError,
            ParametroFaltanteError,
            ServicioNoDisponibleError
        ) as error:
            messagebox.showerror("Error", str(error))

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    boton_procesar.config(command=procesar_reserva)

    etiqueta = ttk.Label(marco, text="Pestaña Reservas – en construcción (Estudiante 4)")  # Texto temporal
    etiqueta.pack(pady=20)  # Ubica la etiqueta en el marco con espacio vertical
    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

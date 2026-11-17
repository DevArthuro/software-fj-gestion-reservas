"""
Archivo: src/interfaz/pestana_reservas.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 4

Interfaz gráfica para crear reservas (cliente + servicio + duración) y para
confirmarlas, cancelarlas y procesarlas. Cada error se registra en
logs/sistema.log y se muestra al usuario.

IMPORTANTE: el nombre de la función crear_pestana_reservas y sus parámetros
(contenedor, gestor) no se pueden cambiar, porque la ventana principal la
llama exactamente así.
"""

import tkinter as tk  # Librería gráfica
from tkinter import ttk, messagebox  # Widgets con estilo y ventanas emergentes

from src.reserva import Reserva  # Clase Reserva
from src.excepciones import (  # Excepciones personalizadas que puede mostrar esta pestaña
    ReservaInvalidaError,  # Reserva inválida u operación no permitida
    ParametroFaltanteError,  # Falta un dato obligatorio
    ServicioNoDisponibleError,  # El servicio está bloqueado
    CalculoInconsistenteError,  # Costo calculado inválido
)
from src.logger import registrar_evento, registrar_error  # Funciones para escribir en el log

ERRORES_PREVISTOS = (  # Errores del modelo que se muestran con su propio mensaje
    ReservaInvalidaError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


def crear_pestana_reservas(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Reservas."""
    marco = ttk.Frame(contenedor, padding=20)  # Marco de la pestaña con margen interno

    def mostrar_error(titulo, mensaje):
        """Registra el error en el log y lo muestra en una ventana."""
        registrar_error(f"Pestaña Reservas - {titulo}: {mensaje}")  # Deja constancia en logs/sistema.log
        marco.update_idletasks()  # Redibuja la tabla antes de abrir la ventana emergente
        messagebox.showerror(titulo, mensaje)  # Muestra la ventana de error

    def mostrar_exito(titulo, mensaje):
        """Registra el evento en el log y muestra un mensaje de confirmación."""
        registrar_evento(f"Pestaña Reservas - {titulo}: {mensaje}")  # Deja constancia en logs/sistema.log
        marco.update_idletasks()  # Redibuja la tabla antes de abrir la ventana emergente
        messagebox.showinfo(titulo, mensaje)  # Muestra la ventana de información

    # ======================================================
    # FORMULARIO PARA REGISTRAR RESERVAS
    # ======================================================

    formulario = ttk.LabelFrame(marco, text="Registrar reserva", padding=15)  # Recuadro del formulario
    formulario.pack(fill="x", pady=(0, 15))  # Ocupa todo el ancho

    ttk.Label(formulario, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Etiqueta cliente
    combo_cliente = ttk.Combobox(formulario, state="readonly", width=40)  # Lista de clientes registrados
    combo_cliente.grid(row=0, column=1, padx=5, pady=5)  # Ubica la lista

    ttk.Label(formulario, text="Servicio:").grid(row=1, column=0, padx=5, pady=5, sticky="w")  # Etiqueta servicio
    combo_servicio = ttk.Combobox(formulario, state="readonly", width=40)  # Lista de servicios registrados
    combo_servicio.grid(row=1, column=1, padx=5, pady=5)  # Ubica la lista

    ttk.Label(formulario, text="Duración (horas):").grid(row=2, column=0, padx=5, pady=5, sticky="w")  # Etiqueta duración
    entrada_duracion = ttk.Entry(formulario, width=43)  # Campo para la duración
    entrada_duracion.grid(row=2, column=1, padx=5, pady=5)  # Ubica el campo

    # ======================================================
    # BOTONES DE ACCIONES
    # ======================================================

    contenedor_botones = ttk.Frame(marco)  # Fila de botones
    contenedor_botones.pack(fill="x", pady=(0, 15))  # Ocupa todo el ancho

    boton_crear = ttk.Button(contenedor_botones, text="Crear reserva")  # Botón crear
    boton_crear.pack(side="left", padx=5)  # Ubica el botón
    boton_confirmar = ttk.Button(contenedor_botones, text="Confirmar")  # Botón confirmar
    boton_confirmar.pack(side="left", padx=5)  # Ubica el botón
    boton_cancelar = ttk.Button(contenedor_botones, text="Cancelar")  # Botón cancelar
    boton_cancelar.pack(side="left", padx=5)  # Ubica el botón
    boton_procesar = ttk.Button(contenedor_botones, text="Procesar")  # Botón procesar
    boton_procesar.pack(side="left", padx=5)  # Ubica el botón

    # ======================================================
    # TABLA DE RESERVAS REGISTRADAS
    # ======================================================

    contenedor_tabla = ttk.LabelFrame(marco, text="Reservas registradas", padding=10)  # Recuadro de la tabla
    contenedor_tabla.pack(fill="both", expand=True, pady=10)  # Ocupa el espacio restante

    encabezados = {  # Columnas de la tabla y su título
        "id": "ID",
        "cliente": "Cliente",
        "servicio": "Servicio",
        "duracion": "Duración (h)",
        "estado": "Estado",
        "costo": "Costo",
    }
    tabla_reservas = ttk.Treeview(  # Tabla de reservas
        contenedor_tabla, columns=tuple(encabezados), show="headings", height=10  # 10 filas visibles
    )
    for columna, texto in encabezados.items():  # Configura cada columna
        tabla_reservas.heading(columna, text=texto)  # Título de la columna
        tabla_reservas.column(columna, width=120, anchor="center")  # Ancho y alineación
    tabla_reservas.pack(fill="both", expand=True)  # Ubica la tabla

    # ======================================================
    # CARGA DE CLIENTES Y SERVICIOS
    # ======================================================

    clientes_disponibles = []  # Clientes que aparecen en la lista desplegable
    servicios_disponibles = []  # Servicios que aparecen en la lista desplegable

    def actualizar_opciones():
        """Actualiza los clientes y servicios de las listas desplegables."""
        clientes_disponibles.clear()  # Vacía la lista anterior
        clientes_disponibles.extend(gestor.listar_clientes())  # Carga los clientes del gestor
        servicios_disponibles.clear()  # Vacía la lista anterior
        servicios_disponibles.extend(gestor.listar_servicios())  # Carga los servicios del gestor

        combo_cliente["values"] = [  # Texto de cada cliente en la lista
            f"{cliente.nombre} - {cliente.documento}" for cliente in clientes_disponibles
        ]
        combo_servicio["values"] = [  # Texto de cada servicio; avisa si no está disponible
            f"{servicio.nombre} - ${servicio.precio_base:,.0f}"
            + ("" if servicio.disponible else " (no disponible)")
            for servicio in servicios_disponibles
        ]
        combo_cliente.set("")  # Limpia la selección de cliente
        combo_servicio.set("")  # Limpia la selección de servicio

    ttk.Button(  # Botón para recargar las listas
        formulario, text="Actualizar clientes y servicios", command=actualizar_opciones
    ).grid(row=3, column=0, columnspan=2, pady=10)  # Ubica el botón bajo el formulario

    actualizar_opciones()  # Carga inicial de las listas

    def obtener_reserva_seleccionada(accion):
        """Retorna la reserva seleccionada en la tabla, o None si no hay selección."""
        seleccion = tabla_reservas.selection()  # Filas seleccionadas
        if not seleccion:  # No hay ninguna fila seleccionada
            registrar_error(f"Pestaña Reservas - {accion}: no se seleccionó ninguna reserva.")  # Queda en el log
            messagebox.showwarning("Seleccionar reserva", "Debe seleccionar una reserva de la tabla.")  # Aviso
            return None  # No hay reserva
        id_reserva = seleccion[0]  # El iid de la fila es el ID de la reserva
        reserva = next(  # Busca la reserva en el gestor
            (reserva for reserva in gestor.listar_reservas() if reserva.id == id_reserva), None
        )
        if reserva is None:  # La fila no corresponde a una reserva registrada
            raise ReservaInvalidaError("No se encontró la reserva seleccionada.")  # Reserva inválida
        return reserva  # Devuelve la reserva encontrada

    # ======================================================
    # ACCIONES
    # ======================================================

    def crear_reserva():
        """Registra una nueva reserva con los datos seleccionados."""
        try:  # Intenta crear la reserva
            indice_cliente = combo_cliente.current()  # Posición del cliente elegido (-1 si ninguno)
            indice_servicio = combo_servicio.current()  # Posición del servicio elegido (-1 si ninguno)
            if indice_cliente < 0:  # No se eligió cliente
                raise ParametroFaltanteError("Debe seleccionar un cliente.")  # Falta el dato
            if indice_servicio < 0:  # No se eligió servicio
                raise ParametroFaltanteError("Debe seleccionar un servicio.")  # Falta el dato

            texto_duracion = entrada_duracion.get().strip()  # Lee la duración
            try:  # Intenta convertir la duración a número
                duracion = float(texto_duracion)  # Duración como decimal
            except ValueError as error:  # El texto no es un número
                raise ReservaInvalidaError("La duración debe ser un número válido.") from error  # Encadenamiento

            cliente = clientes_disponibles[indice_cliente]  # Cliente elegido
            servicio = servicios_disponibles[indice_servicio]  # Servicio elegido
            id_reserva = f"R{len(gestor.reservas) + 1:03d}"  # Genera el ID consecutivo (R001, R002...)

            reserva = Reserva(id_reserva, cliente, servicio, duracion)  # Crea la reserva (valida sus datos)
            gestor.crear_reserva(reserva)  # La registra (revisa duplicados y disponibilidad)

        except ERRORES_PREVISTOS as error:  # Errores del modelo
            mostrar_error("Error al crear reserva", str(error))  # Error al log y pantalla
        except Exception as error:  # Cualquier error no previsto
            mostrar_error("Error inesperado", f"No fue posible crear la reserva. Detalle: {error}")  # Error al log
        else:  # Solo si no hubo errores
            tabla_reservas.insert(  # Agrega la fila a la tabla
                "", "end", iid=reserva.id,  # Usa el ID como identificador de la fila
                values=(reserva.id, cliente.nombre, servicio.nombre, f"{reserva.duracion:g}",
                        reserva.estado, f"${reserva.costo:,.2f}"),  # Datos visibles
            )
            entrada_duracion.delete(0, tk.END)  # Limpia el campo de duración
            mostrar_exito("Reserva creada", f"La reserva {reserva.id} se registró correctamente.")  # Evento

    def confirmar_reserva():
        """Confirma la reserva seleccionada en la tabla."""
        try:  # Intenta confirmar
            reserva = obtener_reserva_seleccionada("Confirmar")  # Reserva elegida
            if reserva is None:  # No había selección
                return  # Detiene la operación
            reserva.confirmar()  # Cambia el estado a confirmada (try/except/else en el modelo)
        except ERRORES_PREVISTOS as error:  # Errores del modelo
            mostrar_error("Error al confirmar reserva", str(error))  # Error al log y pantalla
        except Exception as error:  # Cualquier error no previsto
            mostrar_error("Error inesperado", f"No fue posible confirmar la reserva. Detalle: {error}")  # Error al log
        else:  # Solo si no hubo errores
            tabla_reservas.set(reserva.id, "estado", reserva.estado)  # Actualiza la columna Estado
            mostrar_exito("Reserva confirmada", f"La reserva {reserva.id} se confirmó correctamente.")  # Evento

    def cancelar_reserva():
        """Cancela la reserva seleccionada en la tabla."""
        try:  # Intenta cancelar
            reserva = obtener_reserva_seleccionada("Cancelar")  # Reserva elegida
            if reserva is None:  # No había selección
                return  # Detiene la operación
            reserva.cancelar()  # Cambia el estado a cancelada (try/except/finally en el modelo)
        except ERRORES_PREVISTOS as error:  # Errores del modelo
            mostrar_error("Error al cancelar reserva", str(error))  # Error al log y pantalla
        except Exception as error:  # Cualquier error no previsto
            mostrar_error("Error inesperado", f"No fue posible cancelar la reserva. Detalle: {error}")  # Error al log
        else:  # Solo si no hubo errores
            tabla_reservas.set(reserva.id, "estado", reserva.estado)  # Actualiza la columna Estado
            mostrar_exito("Reserva cancelada", f"La reserva {reserva.id} se canceló correctamente.")  # Evento

    def procesar_reserva():
        """Calcula el costo de la reserva seleccionada."""
        try:  # Intenta procesar
            reserva = obtener_reserva_seleccionada("Procesar")  # Reserva elegida
            if reserva is None:  # No había selección
                return  # Detiene la operación
            costo = reserva.procesar()  # Calcula el costo (raise ... from en el modelo)
        except ERRORES_PREVISTOS as error:  # Errores del modelo
            mostrar_error("Error al procesar reserva", str(error))  # Error al log y pantalla
        except Exception as error:  # Cualquier error no previsto
            mostrar_error("Error inesperado", f"No fue posible procesar la reserva. Detalle: {error}")  # Error al log
        else:  # Solo si no hubo errores
            tabla_reservas.set(reserva.id, "costo", f"${costo:,.2f}")  # Actualiza la columna Costo
            mostrar_exito("Reserva procesada", f"El costo de la reserva {reserva.id} es ${costo:,.2f}")  # Evento

    boton_crear.config(command=crear_reserva)  # Conecta el botón Crear
    boton_confirmar.config(command=confirmar_reserva)  # Conecta el botón Confirmar
    boton_cancelar.config(command=cancelar_reserva)  # Conecta el botón Cancelar
    boton_procesar.config(command=procesar_reserva)  # Conecta el botón Procesar

    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

"""
Archivo: src/interfaz/pestana_servicios.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 3

Interfaz gráfica para crear servicios (sala, equipo o asesoría), ver la tabla
de servicios con su estado, cambiar su disponibilidad y calcular costos con
impuesto y descuento opcionales. Cada error se registra en logs/sistema.log.

IMPORTANTE: el nombre de la función crear_pestana_servicios y sus parámetros
(contenedor, gestor) no se pueden cambiar, porque la ventana principal la
llama exactamente así.
"""

import math  # Permite verificar que los números sean finitos
import tkinter as tk  # Librería gráfica
from tkinter import ttk, messagebox  # Widgets con estilo y ventanas emergentes

from src.servicios import ReservaSala, AlquilerEquipo, Asesoria  # Los tres servicios especializados
from src.excepciones import (  # Excepciones personalizadas que puede mostrar esta pestaña
    ServicioInvalidoError,  # Datos de servicio inválidos o ID repetido
    CalculoInconsistenteError,  # Horas o porcentajes inválidos
    ParametroFaltanteError,  # Falta un dato obligatorio
)
from src.logger import registrar_evento, registrar_error  # Funciones para escribir en el log


def crear_pestana_servicios(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Servicios."""
    marco = ttk.Frame(contenedor, padding=20)  # Marco de la pestaña con margen interno

    def mostrar_error(titulo, mensaje):
        """Registra el error en el log y lo muestra en una ventana."""
        registrar_error(f"Pestaña Servicios - {titulo}: {mensaje}")  # Deja constancia en logs/sistema.log
        marco.update_idletasks()  # Redibuja la tabla antes de abrir la ventana emergente
        messagebox.showerror(titulo, mensaje)  # Muestra la ventana de error

    def mostrar_exito(titulo, mensaje):
        """Registra el evento en el log y muestra un mensaje de confirmación."""
        registrar_evento(f"Pestaña Servicios - {titulo}: {mensaje}")  # Deja constancia en logs/sistema.log
        marco.update_idletasks()  # Redibuja la tabla antes de abrir la ventana emergente
        messagebox.showinfo(titulo, mensaje)  # Muestra la ventana de información

    titulo = ttk.Label(marco, text="Gestión de Servicios", font=("Arial", 16, "bold"))  # Título de la pestaña
    titulo.pack(pady=10)  # Ubica el título con espacio vertical

    contenedor_superior = ttk.Frame(marco)  # Agrupa el formulario y la calculadora
    contenedor_superior.pack(fill="x")  # Ocupa todo el ancho

    contenedor_formulario = ttk.Frame(contenedor_superior)  # Columna izquierda: formulario
    contenedor_formulario.pack(side="left", padx=20, anchor="n")  # Se ubica a la izquierda

    contenedor_calculadora = ttk.Frame(contenedor_superior)  # Columna derecha: calculadora
    contenedor_calculadora.pack(side="right", padx=20, anchor="n")  # Se ubica a la derecha

    # ======================================================
    # FORMULARIO PARA CREAR SERVICIOS
    # ======================================================

    ttk.Label(contenedor_formulario, text="Tipo de servicio:").pack(pady=5)  # Etiqueta del tipo
    tipo_servicio = ttk.Combobox(  # Lista desplegable con los tres tipos de servicio
        contenedor_formulario,
        values=["Reserva de sala", "Alquiler de equipo", "Asesoría"],  # Opciones disponibles
        state="readonly",  # Solo se puede elegir, no escribir
    )
    tipo_servicio.pack(pady=5)  # Ubica la lista desplegable
    tipo_servicio.current(0)  # Selecciona "Reserva de sala" por defecto

    ttk.Label(contenedor_formulario, text="ID del servicio:").pack(pady=5)  # Etiqueta del ID
    entrada_id = ttk.Entry(contenedor_formulario)  # Campo para el ID
    entrada_id.pack(pady=5)  # Ubica el campo

    ttk.Label(contenedor_formulario, text="Nombre del servicio:").pack(pady=5)  # Etiqueta del nombre
    entrada_nombre = ttk.Entry(contenedor_formulario)  # Campo para el nombre
    entrada_nombre.pack(pady=5)  # Ubica el campo

    ttk.Label(contenedor_formulario, text="Precio por hora:").pack(pady=5)  # Etiqueta del precio
    entrada_precio = ttk.Entry(contenedor_formulario)  # Campo para el precio
    entrada_precio.pack(pady=5)  # Ubica el campo

    etiqueta_capacidad = ttk.Label(contenedor_formulario, text="Capacidad de la sala:")  # Solo para salas
    entrada_capacidad = ttk.Entry(contenedor_formulario)  # Campo para la capacidad

    etiqueta_equipo = ttk.Label(contenedor_formulario, text="Tipo de equipo:")  # Solo para equipos
    entrada_equipo = ttk.Entry(contenedor_formulario)  # Campo para el tipo de equipo

    etiqueta_especialidad = ttk.Label(contenedor_formulario, text="Especialidad de la asesoría:")  # Solo para asesorías
    entrada_especialidad = ttk.Entry(contenedor_formulario)  # Campo para la especialidad

    campos_especificos = {  # Relaciona cada tipo con su etiqueta y su campo
        "Reserva de sala": (etiqueta_capacidad, entrada_capacidad),  # Sala -> capacidad
        "Alquiler de equipo": (etiqueta_equipo, entrada_equipo),  # Equipo -> tipo de equipo
        "Asesoría": (etiqueta_especialidad, entrada_especialidad),  # Asesoría -> especialidad
    }

    def actualizar_campos(event=None):
        """Muestra solo el campo correspondiente al tipo de servicio seleccionado."""
        for etiqueta, entrada in campos_especificos.values():  # Recorre los tres campos específicos
            etiqueta.pack_forget()  # Oculta la etiqueta
            entrada.pack_forget()  # Oculta el campo
        etiqueta, entrada = campos_especificos[tipo_servicio.get()]  # Campo del tipo elegido
        etiqueta.pack(pady=5, before=boton_crear)  # Muestra la etiqueta antes del botón
        entrada.pack(pady=5, before=boton_crear)  # Muestra el campo antes del botón

    tipo_servicio.bind("<<ComboboxSelected>>", actualizar_campos)  # Cambia los campos al elegir otro tipo

    def crear_servicio():
        """Valida el formulario, crea el servicio y lo registra en el gestor."""
        identificador = entrada_id.get().strip()  # Lee el ID sin espacios
        nombre = entrada_nombre.get().strip()  # Lee el nombre sin espacios
        precio = entrada_precio.get().strip()  # Lee el precio como texto
        seleccion = tipo_servicio.get()  # Tipo de servicio elegido

        if not identificador or not nombre or not precio:  # Falta algún dato general
            mostrar_error("Datos incompletos", "Debes ingresar el ID, nombre y precio del servicio.")  # Error al log y pantalla
            return  # Detiene la creación

        try:  # Intenta convertir el precio a número
            precio_base = float(precio)  # Convierte el texto a decimal
        except ValueError:  # El texto no es un número
            mostrar_error("Precio inválido", "El precio debe ser un número válido.")  # Error al log y pantalla
            return  # Detiene la creación

        if not math.isfinite(precio_base) or precio_base <= 0:  # Precio negativo, cero o infinito
            mostrar_error("Precio inválido", "El precio debe ser un número mayor que cero.")  # Error al log y pantalla
            return  # Detiene la creación

        dato_especifico = campos_especificos[seleccion][1].get().strip()  # Lee el campo propio del tipo
        if not dato_especifico:  # El campo específico está vacío
            mostrar_error("Datos incompletos", "Debes completar el campo específico del servicio.")  # Error al log y pantalla
            return  # Detiene la creación

        try:  # Intenta crear y registrar el servicio
            if seleccion == "Reserva de sala":  # Se creará una sala
                try:  # Intenta convertir la capacidad a entero
                    capacidad = int(dato_especifico)  # Convierte el texto a entero
                except ValueError as error:  # El texto no es un entero
                    raise ServicioInvalidoError("La capacidad debe ser un número entero.") from error  # Encadenamiento
                servicio = ReservaSala(identificador, nombre, precio_base, capacidad)  # Crea la sala
            elif seleccion == "Alquiler de equipo":  # Se creará un alquiler de equipo
                servicio = AlquilerEquipo(identificador, nombre, precio_base, dato_especifico)  # Crea el alquiler
            else:  # Se creará una asesoría
                servicio = Asesoria(identificador, nombre, precio_base, dato_especifico)  # Crea la asesoría
            gestor.agregar_servicio(servicio)  # Valida y guarda en el gestor (detecta ID repetido)
        except (ServicioInvalidoError, CalculoInconsistenteError, ParametroFaltanteError) as error:  # Errores previstos
            mostrar_error("Error al registrar servicio", str(error))  # Error al log y pantalla
            return  # Detiene la creación
        except Exception as error:  # Cualquier error no previsto
            mostrar_error("Error inesperado", f"No fue posible registrar el servicio. Detalle: {error}")  # Error al log y pantalla
            return  # Detiene la creación

        tabla_servicios.insert(  # Agrega una fila a la tabla
            "", "end", iid=servicio.id,  # Usa el ID como identificador de la fila
            values=(servicio.id, seleccion, nombre, f"${precio_base:,.0f}", "Disponible"),  # Datos visibles
        )
        for entrada in (entrada_id, entrada_nombre, entrada_precio, campos_especificos[seleccion][1]):  # Campos usados
            entrada.delete(0, tk.END)  # Limpia cada campo
        mostrar_exito("Servicio registrado", f"El servicio {servicio.id} se registró correctamente.")  # Evento al log y pantalla

    boton_crear = ttk.Button(contenedor_formulario, text="Crear servicio", command=crear_servicio)  # Botón para crear
    boton_crear.pack(pady=15)  # Ubica el botón

    actualizar_campos()  # Muestra el campo inicial (capacidad de la sala)

    # ======================================================
    # TABLA DE SERVICIOS REGISTRADOS
    # ======================================================

    ttk.Label(marco, text="Servicios registrados", font=("Arial", 12, "bold")).pack(pady=(10, 5))  # Título de la tabla

    columnas = ("ID", "Tipo", "Nombre", "Precio", "Estado")  # Columnas de la tabla
    tabla_servicios = ttk.Treeview(marco, columns=columnas, show="headings", height=5)  # Tabla de 5 filas visibles
    encabezados = {  # Texto y ancho de cada columna
        "ID": ("ID", 80),  # Columna del ID
        "Tipo": ("Tipo de servicio", 150),  # Columna del tipo
        "Nombre": ("Nombre", 200),  # Columna del nombre
        "Precio": ("Precio por hora", 120),  # Columna del precio
        "Estado": ("Estado", 120),  # Columna de disponibilidad
    }
    for columna, (texto, ancho) in encabezados.items():  # Configura cada columna
        tabla_servicios.heading(columna, text=texto)  # Título de la columna
        tabla_servicios.column(columna, width=ancho, anchor="center")  # Ancho y alineación
    tabla_servicios.pack(pady=5, padx=5, fill="x")  # Ubica la tabla a todo el ancho

    def cambiar_disponibilidad():
        """Alterna el servicio seleccionado entre disponible y no disponible."""
        seleccion_tabla = tabla_servicios.selection()  # Filas seleccionadas
        if not seleccion_tabla:  # No hay ninguna fila seleccionada
            mostrar_error("Seleccionar servicio", "Debes seleccionar un servicio de la tabla.")  # Error al log y pantalla
            return  # Detiene la operación
        id_servicio = seleccion_tabla[0]  # El iid de la fila es el ID del servicio
        servicio = gestor.buscar_servicio(id_servicio)  # Busca el servicio en el gestor
        try:  # Intenta cambiar el estado
            if servicio is None:  # La fila no corresponde a un servicio registrado
                raise ServicioInvalidoError("No se encontró el servicio seleccionado.")  # Servicio inválido
            gestor.cambiar_disponibilidad_servicio(id_servicio, not servicio.disponible)  # Invierte el estado
        except (ServicioInvalidoError, ParametroFaltanteError) as error:  # Errores previstos
            mostrar_error("Error de disponibilidad", str(error))  # Error al log y pantalla
            return  # Detiene la operación
        estado = "Disponible" if servicio.disponible else "No disponible"  # Texto del nuevo estado
        tabla_servicios.set(id_servicio, "Estado", estado)  # Actualiza la columna Estado
        mostrar_exito("Disponibilidad actualizada", f"El servicio {id_servicio} ahora está: {estado}.")  # Evento al log y pantalla

    ttk.Button(marco, text="Cambiar disponibilidad", command=cambiar_disponibilidad).pack(pady=5)  # Botón bajo la tabla

    # ======================================================
    # CALCULADORA DE COSTOS (sobrecarga con parámetros opcionales)
    # ======================================================

    ttk.Label(contenedor_calculadora, text="Calculadora de costos", font=("Arial", 12, "bold")).pack(pady=10)  # Título

    ttk.Label(contenedor_calculadora, text="Cantidad de horas:").pack(pady=5)  # Etiqueta de horas
    entrada_horas = ttk.Entry(contenedor_calculadora)  # Campo para las horas
    entrada_horas.pack(pady=5)  # Ubica el campo

    ttk.Label(contenedor_calculadora, text="Impuesto (%):").pack(pady=5)  # Etiqueta del impuesto
    entrada_impuesto = ttk.Entry(contenedor_calculadora)  # Campo para el impuesto (opcional)
    entrada_impuesto.pack(pady=5)  # Ubica el campo

    ttk.Label(contenedor_calculadora, text="Descuento (%):").pack(pady=5)  # Etiqueta del descuento
    entrada_descuento = ttk.Entry(contenedor_calculadora)  # Campo para el descuento (opcional)
    entrada_descuento.pack(pady=5)  # Ubica el campo

    def calcular_costo():
        """Calcula el costo del servicio seleccionado con impuesto y descuento opcionales."""
        horas_texto = entrada_horas.get().strip()  # Lee las horas
        impuesto_texto = entrada_impuesto.get().strip()  # Lee el impuesto
        descuento_texto = entrada_descuento.get().strip()  # Lee el descuento

        if not horas_texto:  # No se escribieron horas
            mostrar_error("Datos incompletos", "Debes ingresar la cantidad de horas.")  # Error al log y pantalla
            return  # Detiene el cálculo

        try:  # Intenta convertir los textos a números
            horas = float(horas_texto)  # Horas como decimal
            impuesto = float(impuesto_texto) if impuesto_texto else 0  # Impuesto o 0 si está vacío
            descuento = float(descuento_texto) if descuento_texto else 0  # Descuento o 0 si está vacío
        except ValueError:  # Algún texto no es un número
            mostrar_error("Datos inválidos", "Las horas, el impuesto y el descuento deben ser números válidos.")  # Error al log
            return  # Detiene el cálculo

        seleccion_tabla = tabla_servicios.selection()  # Filas seleccionadas
        if not seleccion_tabla:  # No hay servicio seleccionado
            mostrar_error("Seleccionar servicio", "Debes seleccionar un servicio de la tabla.")  # Error al log y pantalla
            return  # Detiene el cálculo

        servicio = gestor.buscar_servicio(seleccion_tabla[0])  # Busca el servicio por el ID de la fila
        if servicio is None:  # La fila no corresponde a un servicio registrado
            mostrar_error("Servicio no encontrado", "No se encontró el servicio seleccionado.")  # Error al log y pantalla
            return  # Detiene el cálculo

        try:  # Intenta calcular el costo (el modelo valida horas y porcentajes)
            costo_total = servicio.calcular_costo(horas, impuesto, descuento)  # Polimorfismo: cada hija calcula
        except (ServicioInvalidoError, CalculoInconsistenteError) as error:  # Cálculo inválido
            mostrar_error("Error al calcular", str(error))  # Error al log y pantalla
            return  # Detiene el cálculo

        mostrar_exito(  # Evento al log y pantalla
            "Costo del servicio",
            f"{servicio.describir()}\n\nHoras: {horas:g} | Impuesto: {impuesto:g}% | Descuento: {descuento:g}%\n"
            f"Costo total: ${costo_total:,.2f}",  # Detalle del cálculo
        )

    ttk.Button(contenedor_calculadora, text="Calcular costo", command=calcular_costo).pack(pady=10)  # Botón calcular

    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

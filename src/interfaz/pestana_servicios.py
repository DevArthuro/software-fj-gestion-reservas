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

import math
import tkinter as tk
from tkinter import ttk, messagebox

from src.servicios import ReservaSala, AlquilerEquipo, Asesoria
from src.excepciones import ServicioInvalidoError, CalculoInconsistenteError 


def crear_pestana_servicios(contenedor, gestor):
    """Crea y retorna el marco de la pestaña Servicios. La completa el Estudiante 3."""
    marco = ttk.Frame(contenedor, padding=20) # Crea el marco de la pestaña con margen interno
    titulo = ttk.Label(
        marco,
        text="Gestión de Servicios",
        font=("Arial", 16, "bold")
    )
    titulo.pack(pady=10)
    
    contenedor_superior = ttk.Frame(marco)
    contenedor_superior.pack(fill="x")
    
    contenedor_formulario = ttk.Frame(contenedor_superior)
    contenedor_formulario.pack(
        side="left", 
        padx=20, 
        anchor="n"
    )
    
    contenedor_calculadora = ttk.Frame(contenedor_superior)
    contenedor_calculadora.pack(
        side="right",
        padx=20,
        anchor="n"
    )

    etiqueta_tipo = ttk.Label(
        contenedor_formulario,
        text="Tipo de servicio:"
    )
    etiqueta_tipo.pack(pady=5)

    tipo_servicio = ttk.Combobox(
        contenedor_formulario,
        values=[
            "Reserva de sala",
            "Alquiler de equipo",
            "Asesoría"
        ],
        state="readonly"
    )
    tipo_servicio.pack(pady=5)
    tipo_servicio.current(0)

    etiqueta_id = ttk.Label(
        contenedor_formulario,
        text="ID del servicio:"
    )
    etiqueta_id.pack(pady=5)

    entrada_id = ttk.Entry(contenedor_formulario)
    entrada_id.pack(pady=5)

    etiqueta_nombre = ttk.Label(
        contenedor_formulario,
        text="Nombre del servicio:"
    )
    etiqueta_nombre.pack(pady=5)

    entrada_nombre = ttk.Entry(contenedor_formulario)
    entrada_nombre.pack(pady=5)

    etiqueta_precio = ttk.Label(
        contenedor_formulario,
        text="Precio por hora:"
    )
    etiqueta_precio.pack(pady=5)

    entrada_precio = ttk.Entry(contenedor_formulario)
    entrada_precio.pack(pady=5)

    etiqueta_capacidad = ttk.Label(
        contenedor_formulario,
        text="Capacidad de la sala:"
    )
    etiqueta_capacidad.pack(pady=5)

    entrada_capacidad = ttk.Entry(contenedor_formulario)
    entrada_capacidad.pack(pady=5)

    etiqueta_equipo = ttk.Label(
        contenedor_formulario, 
        text="Tipo de equipo:"
    )
    etiqueta_equipo.pack(pady=5)

    entrada_equipo = ttk.Entry(contenedor_formulario)
    entrada_equipo.pack(pady=5)

    etiqueta_especialidad = ttk.Label(
        contenedor_formulario,
        text="Especialidad de la asesoría:"
    )
    etiqueta_especialidad.pack(pady=5)

    entrada_especialidad = ttk.Entry(contenedor_formulario)
    entrada_especialidad.pack(pady=5)

    def actualizar_campos(event=None):
        """Muestra el campo correspondiente al servicio seleccionado."""

        etiqueta_capacidad.pack_forget()
        entrada_capacidad.pack_forget()

        etiqueta_equipo.pack_forget()
        entrada_equipo.pack_forget()

        etiqueta_especialidad.pack_forget()
        entrada_especialidad.pack_forget()

        seleccion = tipo_servicio.get()
     
        if seleccion == "Reserva de sala":
            etiqueta_capacidad.pack(
                pady=5,
                before=boton_crear
            )
            entrada_capacidad.pack(
                pady=5,
                before=boton_crear
            )

        elif seleccion == "Alquiler de equipo":
            etiqueta_equipo.pack(
                pady=5,
                before=boton_crear
            )
            entrada_equipo.pack(
                pady=5,
                before=boton_crear
            )

        elif seleccion == "Asesoría":
            etiqueta_especialidad.pack(
                pady=5,
                before=boton_crear
            )
            entrada_especialidad.pack(
                pady=5,
                before=boton_crear
            )

    tipo_servicio.bind("<<ComboboxSelected>>", actualizar_campos) 

    def crear_servicio():
        """Obtiene los datos ingresados en el formulario."""

        identificador = entrada_id.get().strip()
        nombre = entrada_nombre.get().strip()
        precio = entrada_precio.get().strip()
        seleccion = tipo_servicio.get()

        
        if not identificador or not nombre or not precio:
            messagebox.showerror(
                "Datos incompletos",
                "Debes ingresar el ID, nombre y precio del servicio."
            )
            return
   
        try:
            precio_base = float(precio)
        except ValueError:
            messagebox.showerror(
                "Precio inválido",
                "El precio debe ser un número válido."
            )
            return

        
        if not math.isfinite(precio_base) or precio_base <= 0:
            messagebox.showerror(
                "Precio inválido",
                "El precio debe ser un número mayor que cero."
            )
            return
    
        if seleccion == "Reserva de sala":
            dato_especifico = entrada_capacidad.get().strip()

        elif seleccion == "Alquiler de equipo":
            dato_especifico = entrada_equipo.get().strip()

        elif seleccion == "Asesoría":
            dato_especifico = entrada_especialidad.get().strip()
  
        if not dato_especifico:
            messagebox.showerror(
                "Datos incompletos",
                "Debes completar el campo específico del servicio."
            )
            return
        
        if seleccion == "Reserva de sala":
            try:
                capacidad = int(dato_especifico)

                servicio = ReservaSala(
                    identificador,
                    nombre,
                    precio_base,
                    capacidad
                )

            except ValueError:
                messagebox.showerror(
                    "Capacidad inválida",
                    "La capacidad debe ser un número entero."
                )
                return
        
        elif seleccion == "Alquiler de equipo":
            servicio = AlquilerEquipo(
                identificador,
                nombre,
                precio_base,
                dato_especifico
            )
        
        elif seleccion == "Asesoría":
            servicio = Asesoria(
                identificador,
                nombre,
                precio_base,
                dato_especifico
            )
          
        try:
            gestor.agregar_servicio(servicio)

        except (ServicioInvalidoError, CalculoInconsistenteError) as error:
            messagebox.showerror(
                "Error al registrar servicio",
                str(error)
            )
            return

        messagebox.showinfo(
            "Servicio registrado",
            "El servicio se registró correctamente."
        )
        
        tabla_servicios.insert(
            "",
            "end",
            values=(
                identificador,
                seleccion,
                nombre,
                f"${precio_base:,.0f}"
            )
        )

    boton_crear = ttk.Button(
        contenedor_formulario,
        text="Crear servicio",
        command=crear_servicio
        )
    boton_crear.pack(pady=15)
    
    actualizar_campos()
    
    etiqueta_tabla = ttk.Label(
        marco,
        text="Servicios registrados",
        font=("Arial", 12, "bold")
    )
    etiqueta_tabla.pack(pady=10)
    
    tabla_servicios = ttk.Treeview(
        marco,
        columns=("ID", "Tipo", "Nombre", "Precio"),
        show="headings",
        height=3
    )
    
    tabla_servicios.heading("ID", text="ID")
    tabla_servicios.heading("Tipo", text="Tipo de servicio")
    tabla_servicios.heading("Nombre", text="Nombre")
    tabla_servicios.heading("Precio", text="Precio por hora")
    
    tabla_servicios.column("ID", width=80, anchor="center")
    tabla_servicios.column("Tipo", width=150, anchor="center")
    tabla_servicios.column("Nombre", width=200, anchor="center")
    tabla_servicios.column("Precio", width=120, anchor="center")
    
    tabla_servicios.pack(
        pady=5,
        padx=5,
        fill="x",
        expand=True
    )
    
    etiqueta_calculadora = ttk.Label(
        contenedor_calculadora,
        text="Calculadora de costos",
        font=("Arial", 12, "bold")
    )
    etiqueta_calculadora.pack(pady=10)
    
    etiqueta_horas = ttk.Label(
        contenedor_calculadora,
        text="Cantidad de horas:"
    )
    etiqueta_horas.pack(pady=5)

    entrada_horas = ttk.Entry(contenedor_calculadora)
    entrada_horas.pack(pady=5)
    
    etiqueta_impuesto = ttk.Label(
        contenedor_calculadora,
        text="Impuesto (%):"
    )
    etiqueta_impuesto.pack(pady=5)

    entrada_impuesto = ttk.Entry(contenedor_calculadora)
    entrada_impuesto.pack(pady=5)
    
    etiqueta_descuento = ttk.Label(
        contenedor_calculadora,
        text="Descuento (%):"
    )
    etiqueta_descuento.pack(pady=5)

    entrada_descuento = ttk.Entry(contenedor_calculadora)
    entrada_descuento.pack(pady=5)
    
    def calcular_costo():
        """Obtiene los datos para calcular el costo del servicio."""

        horas_texto = entrada_horas.get().strip()
        impuesto_texto = entrada_impuesto.get().strip()
        descuento_texto = entrada_descuento.get().strip()
        
        if not horas_texto:
            messagebox.showerror(
                "Error",
                "Debes ingresar la cantidad de horas."
            )
            return
        
        try:
            horas = float(horas_texto)
            impuesto = float(impuesto_texto) if impuesto_texto else 0
            descuento = float(descuento_texto) if descuento_texto else 0

        except ValueError:
            messagebox.showerror(
                "Error",
                "Las horas, el impuesto y el descuento deben ser números válidos."
            )
            return
        
        if (
            not math.isfinite(horas)
            or horas <= 0
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 100
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            messagebox.showerror(
                "Error",
                "Las horas deben ser mayores que cero y los porcentajes deben estar entre 0 y 100."
            )
            return
        
        seleccion_tabla = tabla_servicios.selection()

        if not seleccion_tabla:
            messagebox.showerror(
                "Error",
                "Debes seleccionar un servicio de la tabla."
            )
            return
        
        fila_seleccionada = seleccion_tabla[0]

        datos_servicio = tabla_servicios.item(
            fila_seleccionada,
            "values"
        )

        id_servicio = datos_servicio[0]
        
        servicio_encontrado = None

        for servicio in gestor.listar_servicios():
            if servicio.id == id_servicio:
                servicio_encontrado = servicio
                break
            
        if servicio_encontrado is None:
            messagebox.showerror(
                "Error",
                "No se encontró el servicio seleccionado."
            )
            return

        try:
            costo_total = servicio_encontrado.calcular_costo(
                horas,
                impuesto,
                descuento
            )

        except (ServicioInvalidoError, CalculoInconsistenteError) as error:
            messagebox.showerror(
                "Error al calcular",
                str(error)
            )
            return
        
        messagebox.showinfo(
            "Costo del servicio",
            f"El costo total del servicio es: ${costo_total:,.0f}"
        )

    boton_calcular = ttk.Button(
        contenedor_calculadora,
        text="Calcular costo",
        command=calcular_costo
    )
    boton_calcular.pack(pady=10)

    return marco  # Retorna el marco para agregarlo al cuaderno de pestañas

    
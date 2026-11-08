# ==========================================================
# Archivo: src/servicios.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 3
#
# TODO: Crear la clase abstracta Servicio(Entidad) y las hijas
#       ReservaSala, AlquilerEquipo y Asesoria.
# TODO: Sobrescribir calcular_costo(), describir() y validar_parametros().
# TODO: "Sobrecarga": calcular_costo(horas, impuesto=0, descuento=0).
# ==========================================================

from abc import ABC  # Para crear clases abstractas
from abc import abstractmethod  # Para marcar métodos abstractos
from src.entidad import Entidad  # Clase de la que hereda Servicio
from src.excepciones import ServicioInvalidoError  # Error para servicios inválidos
from src.excepciones import ServicioNoDisponibleError  # Error para servicios no disponibles
from src.excepciones import CalculoInconsistenteError  # Error para costos inválidos
from src.excepciones import ParametroFaltanteError  # Error para datos obligatorios vacíos
from src.logger import registrar_evento  # Para registrar eventos en el log
from src.logger import registrar_error  # Para registrar errores en el log

import math

class Servicio(Entidad, ABC):
    """Clase abstracta que representa un servicio de Software FJ."""

    def __init__(self, id_servicio, nombre, precio_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.precio_base = precio_base

    def describir(self):
        """Retorna la descripción general del servicio."""
        return f"Servicio: {self.nombre}"

    def validar(self):
        """Verifica que los datos generales sean correctos."""
        if not self.nombre or not self.nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio")
   
        if (
            not isinstance(self.precio_base, (int, float))
            or isinstance(self.precio_base, bool)
            or not math.isfinite(self.precio_base)
            or self.precio_base <= 0
        ):  
            raise ServicioInvalidoError(
                "El precio base debe ser un número mayor que cero."
            )

        @abstractmethod
        def calcular_costo(self, horas, impuesto=0, descuento=0):
            """Calcula el costo del servicio"""

            pass

        @abstractmethod
        def validar_parametros(self):
            """Valida los parámetros específicos del servicio."""

            pass

class ReservaSala(Servicio):
    """Representa el servicio de reserva de salas."""

    def __init__(self, id_servicio, nombre, precio_base, capacidad):
        super().__init__(id_servicio, nombre, precio_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de reservar una sala."""   
        if (
            not isinstance(horas, (int, float))
            or isinstance(horas, bool)
            or not math.isfinite(horas)
            or horas <= 0
        ):
            raise CalculoInconsistenteError(
                "La cantidad de horas debe ser mayor que cero."
            )

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 100
            or not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise CalculoInconsistenteError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        subtotal = self.precio_base * horas
        total = subtotal * (1 + impuesto / 100)
        total = total * (1 - descuento / 100)

        return round(total, 2) 

    def describir(self):
        """Retorna la descripción del servicio de reserva de sala."""
        return (
            f"Reserva de sala: {self.nombre} | "
            f"Precio por hora: ${self.precio_base:,.0f} | "
            f"Capacidad: {self.capacidad} personas"
        )

    def validar_parametros(self):
        """Valida la capacidad de la sala."""
        self.validar()

        if not isinstance(self.capacidad, int) or isinstance(self.capacidad, bool) or self.capacidad <= 0:
            raise ServicioInvalidoError(
                "La capacidad de la sala debe ser un número entero mayor que cero."
            )

class AlquilerEquipo(Servicio):
    """Representa el servicio de alquiler equipos."""

    def __init__(self, id_servicio, nombre, precio_base, tipo_equipo):
        super().__init__(id_servicio, nombre, precio_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo del alquiler de un equipo."""  
            
        if (
            not isinstance(horas, (int, float))
            or isinstance(horas, bool)
            or not math.isfinite(horas)
            or horas <= 0
        ):
            raise CalculoInconsistenteError(
                "La cantidad de horas debe ser mayor que cero."
            )
      
        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 100
            or not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise CalculoInconsistenteError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        subtotal = self.precio_base * horas
        total = subtotal * (1 + impuesto / 100)
        total = total * (1 - descuento / 100)

        return round(total, 2)

    def describir(self):
        """Retorna la descripción del servicio de alquiler de equipos."""
        return (
            f"Alquiler de equipo: {self.nombre} | "
            f"Tipo de equipo: {self.tipo_equipo} | "
            f"Precio por hora: ${self.precio_base:,.0f}"
        )

    def validar_parametros(self):
        """Valida los datos específicos del equipo."""
        self.validar()

        if not isinstance(self.tipo_equipo, str) or not self.tipo_equipo.strip():
            raise ServicioInvalidoError(
                "El tipo de equipo es obligatorio y debe ser un texto válido."
            )

class Asesoria(Servicio):
    """Representa el servicio de asesoría."""

    def __init__(self, id_servicio, nombre, precio_base, especialidad):
        super().__init__(id_servicio, nombre, precio_base)
        self.especialidad = especialidad 

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de una asesoría."""   
        if (
            not isinstance(horas, (int, float))
            or isinstance(horas, bool)
            or not math.isfinite(horas)
            or horas <= 0
        ):
            raise CalculoInconsistenteError(
                "La cantidad de horas debe ser mayor que cero."
            )
         
        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 100
            or not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise CalculoInconsistenteError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        subtotal = self.precio_base * horas
        total = subtotal * (1 + impuesto / 100)
        total = total * (1 - descuento / 100)

        return round(total, 2)

    def describir(self):
        """Retorna la descripción del servicio de asesoría."""
        return (
            f"Asesoría: {self.nombre} | "
            f"Especialidad: {self.especialidad} | "
            f"Precio por hora: ${self.precio_base:,.0f}"
        )

    def validar_parametros(self):
        """Valida los datos específicos de la asesoría."""
        self.validar()

        if not isinstance(self.especialidad, str) or not self.especialidad.strip():
            raise ServicioInvalidoError(
                "La especialidad de la asesoría es obligatorio y debe ser un texto válido."
            )
        
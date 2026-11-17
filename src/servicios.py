"""
Archivo: src/servicios.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 3

Clase abstracta Servicio y sus tres servicios especializados:
ReservaSala, AlquilerEquipo y Asesoria. Cada hija sobrescribe
calcular_costo(), describir() y validar_parametros() (polimorfismo).
calcular_costo(horas, impuesto=0, descuento=0) simula la sobrecarga
de métodos mediante parámetros opcionales.
"""

import math  # Permite verificar que los números sean finitos
from abc import ABC  # Clase base para crear clases abstractas
from abc import abstractmethod  # Decorador para marcar métodos abstractos

from src.entidad import Entidad  # Clase abstracta de la que hereda Servicio
from src.excepciones import ServicioInvalidoError  # Error para servicios con datos inválidos
from src.excepciones import CalculoInconsistenteError  # Error para costos o porcentajes inválidos
from src.logger import registrar_evento  # Para registrar eventos en el log


def _validar_horas(horas):
    """Verifica que la cantidad de horas sea un número mayor que cero."""
    if (  # Revisa todas las condiciones que hacen inválidas las horas
        not isinstance(horas, (int, float))  # Debe ser un número entero o decimal
        or isinstance(horas, bool)  # True/False no cuentan como número
        or not math.isfinite(horas)  # No se aceptan infinito ni NaN
        or horas <= 0  # Debe ser mayor que cero
    ):
        raise CalculoInconsistenteError(  # Lanza el error de cálculo
            "La cantidad de horas debe ser mayor que cero."  # Mensaje para el usuario
        )


def _validar_porcentajes(impuesto, descuento):
    """Verifica que el impuesto y el descuento estén entre 0 y 100."""
    for valor in (impuesto, descuento):  # Revisa los dos porcentajes con la misma regla
        if (  # Revisa las condiciones que hacen inválido el porcentaje
            not isinstance(valor, (int, float))  # Debe ser un número
            or isinstance(valor, bool)  # True/False no cuentan como número
            or not math.isfinite(valor)  # No se aceptan infinito ni NaN
            or not 0 <= valor <= 100  # Debe estar entre 0 y 100
        ):
            raise CalculoInconsistenteError(  # Lanza el error de cálculo
                "El impuesto y el descuento deben estar entre 0 y 100."  # Mensaje para el usuario
            )


def _aplicar_impuesto_y_descuento(subtotal, impuesto, descuento):
    """Aplica el impuesto y luego el descuento a un subtotal y redondea a 2 decimales."""
    total = subtotal * (1 + impuesto / 100)  # Suma el impuesto al subtotal
    total = total * (1 - descuento / 100)  # Resta el descuento al total con impuesto
    if total < 0:  # Un costo nunca puede ser negativo
        raise CalculoInconsistenteError("El costo calculado no puede ser negativo.")  # Cálculo inconsistente
    return round(total, 2)  # Devuelve el total redondeado


class Servicio(Entidad, ABC):
    """Clase abstracta que representa un servicio de Software FJ."""

    def __init__(self, id_servicio, nombre, precio_base):
        """Guarda los datos comunes a todos los servicios."""
        super().__init__(id_servicio)  # Valida y guarda el id en Entidad
        self.nombre = nombre  # Nombre del servicio
        self.precio_base = precio_base  # Precio por hora
        self.disponible = True  # Todo servicio nuevo arranca disponible

    def describir(self):
        """Retorna la descripción general del servicio."""
        return f"Servicio: {self.nombre}"  # Texto básico; las hijas lo sobrescriben

    def validar(self):
        """Verifica que los datos generales sean correctos."""
        if not isinstance(self.nombre, str) or not self.nombre.strip():  # El nombre debe ser un texto no vacío
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")  # Lanza el error

        if (  # Revisa las condiciones que hacen inválido el precio
            not isinstance(self.precio_base, (int, float))  # Debe ser un número
            or isinstance(self.precio_base, bool)  # True/False no cuentan como número
            or not math.isfinite(self.precio_base)  # No se aceptan infinito ni NaN
            or self.precio_base <= 0  # Debe ser mayor que cero
        ):
            raise ServicioInvalidoError(  # Lanza el error de servicio inválido
                "El precio base debe ser un número mayor que cero."  # Mensaje para el usuario
            )

    def cambiar_disponibilidad(self, disponible):
        """Marca el servicio como disponible (True) o no disponible (False)."""
        if not isinstance(disponible, bool):  # Solo se acepta True o False
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")  # Dato inválido
        self.disponible = disponible  # Guarda el nuevo estado
        estado = "disponible" if disponible else "no disponible"  # Texto para el log
        registrar_evento(f"Servicio {self.id} marcado como {estado}.")  # Deja constancia

    @abstractmethod  # Obliga a cada hija a implementar su propio cálculo
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo del servicio."""
        pass  # Lo implementa cada clase hija

    @abstractmethod  # Obliga a cada hija a validar sus datos propios
    def validar_parametros(self):
        """Valida los parámetros específicos del servicio."""
        pass  # Lo implementa cada clase hija


class ReservaSala(Servicio):
    """Representa el servicio de reserva de salas."""

    def __init__(self, id_servicio, nombre, precio_base, capacidad):
        """Crea una sala con su capacidad máxima de personas."""
        super().__init__(id_servicio, nombre, precio_base)  # Guarda los datos comunes en Servicio
        self.capacidad = capacidad  # Número máximo de personas

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de reservar una sala (impuesto y descuento son opcionales)."""
        _validar_horas(horas)  # Verifica la cantidad de horas
        _validar_porcentajes(impuesto, descuento)  # Verifica impuesto y descuento
        subtotal = self.precio_base * horas  # Precio por hora por cantidad de horas
        return _aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)  # Total final

    def describir(self):
        """Retorna la descripción del servicio de reserva de sala."""
        return (  # Arma el texto con los datos de la sala
            f"Reserva de sala: {self.nombre} | "  # Nombre de la sala
            f"Precio por hora: ${self.precio_base:,.0f} | "  # Precio con separador de miles
            f"Capacidad: {self.capacidad} personas"  # Capacidad de la sala
        )

    def validar_parametros(self):
        """Valida los datos generales y la capacidad de la sala."""
        self.validar()  # Primero valida nombre y precio

        if (  # Revisa las condiciones que hacen inválida la capacidad
            not isinstance(self.capacidad, int)  # Debe ser un número entero
            or isinstance(self.capacidad, bool)  # True/False no cuentan como número
            or self.capacidad <= 0  # Debe ser mayor que cero
        ):
            raise ServicioInvalidoError(  # Lanza el error de servicio inválido
                "La capacidad de la sala debe ser un número entero mayor que cero."  # Mensaje para el usuario
            )


class AlquilerEquipo(Servicio):
    """Representa el servicio de alquiler de equipos."""

    def __init__(self, id_servicio, nombre, precio_base, tipo_equipo):
        """Crea un servicio de alquiler con el tipo de equipo."""
        super().__init__(id_servicio, nombre, precio_base)  # Guarda los datos comunes en Servicio
        self.tipo_equipo = tipo_equipo  # Clase de equipo que se alquila

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo del alquiler de un equipo (impuesto y descuento son opcionales)."""
        _validar_horas(horas)  # Verifica la cantidad de horas
        _validar_porcentajes(impuesto, descuento)  # Verifica impuesto y descuento
        subtotal = self.precio_base * horas  # Precio por hora por cantidad de horas
        return _aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)  # Total final

    def describir(self):
        """Retorna la descripción del servicio de alquiler de equipos."""
        return (  # Arma el texto con los datos del equipo
            f"Alquiler de equipo: {self.nombre} | "  # Nombre del equipo
            f"Tipo de equipo: {self.tipo_equipo} | "  # Tipo de equipo
            f"Precio por hora: ${self.precio_base:,.0f}"  # Precio con separador de miles
        )

    def validar_parametros(self):
        """Valida los datos generales y el tipo de equipo."""
        self.validar()  # Primero valida nombre y precio

        if not isinstance(self.tipo_equipo, str) or not self.tipo_equipo.strip():  # Debe ser un texto no vacío
            raise ServicioInvalidoError(  # Lanza el error de servicio inválido
                "El tipo de equipo es obligatorio y debe ser un texto válido."  # Mensaje para el usuario
            )


class Asesoria(Servicio):
    """Representa el servicio de asesoría especializada."""

    def __init__(self, id_servicio, nombre, precio_base, especialidad):
        """Crea una asesoría con su especialidad."""
        super().__init__(id_servicio, nombre, precio_base)  # Guarda los datos comunes en Servicio
        self.especialidad = especialidad  # Área de la asesoría

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de una asesoría (impuesto y descuento son opcionales)."""
        _validar_horas(horas)  # Verifica la cantidad de horas
        _validar_porcentajes(impuesto, descuento)  # Verifica impuesto y descuento
        subtotal = self.precio_base * horas  # Precio por hora por cantidad de horas
        return _aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)  # Total final

    def describir(self):
        """Retorna la descripción del servicio de asesoría."""
        return (  # Arma el texto con los datos de la asesoría
            f"Asesoría: {self.nombre} | "  # Nombre de la asesoría
            f"Especialidad: {self.especialidad} | "  # Especialidad
            f"Precio por hora: ${self.precio_base:,.0f}"  # Precio con separador de miles
        )

    def validar_parametros(self):
        """Valida los datos generales y la especialidad de la asesoría."""
        self.validar()  # Primero valida nombre y precio

        if not isinstance(self.especialidad, str) or not self.especialidad.strip():  # Debe ser un texto no vacío
            raise ServicioInvalidoError(  # Lanza el error de servicio inválido
                "La especialidad de la asesoría es obligatoria y debe ser un texto válido."  # Mensaje para el usuario
            )

# ==========================================================
# Archivo: src/reserva.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 4
#
# TODO: Crear la clase Reserva(Entidad) con cliente, servicio, duración y
#       estado (pendiente / confirmada / cancelada).
# TODO: Métodos confirmar(), cancelar() y procesar() usando try/except/else,
#       try/except/finally y raise ... from e.
# ==========================================================

from src.entidad import Entidad  # Clase de la que hereda Reserva
from src.excepciones import ReservaInvalidaError  # Error para reservas inválidas
from src.excepciones import ServicioNoDisponibleError  # Error si el servicio no está disponible
from src.excepciones import ParametroFaltanteError  # Error para datos obligatorios vacíos
from src.logger import registrar_evento  # Para registrar eventos en el log
from src.logger import registrar_error  # Para registrar errores en el log

import math 


class Reserva(Entidad):
    """Representa una reserva realizada por un cliente."""

    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"
        self.costo = 0

        self.validar()

        registrar_evento(
            f"Reserva creada correctamente. ID: {self.id}"
        )

    def validar(self):
        """Verifica que los datos de la reserva sean correctos."""

        from src.cliente import Cliente
        from src.servicios import Servicio

        if self.cliente is None:
            raise ParametroFaltanteError(
                "Debe seleccionar un cliente para la reserva."
            )

        if not isinstance(self.cliente, Cliente):
            raise ReservaInvalidaError(
                "El cliente seleccionado no es válido."
            )

        if self.servicio is None:
            raise ParametroFaltanteError(
                "Debe seleccionar un servicio para la reserva."
            )

        if not isinstance(self.servicio, Servicio):
            raise ReservaInvalidaError(
                "El servicio seleccionado no es válido."
            )

        if (
            not isinstance(self.duracion, (int, float))
            or isinstance(self.duracion, bool)
            or not math.isfinite(self.duracion)
            or self.duracion <= 0
        ):
            raise ReservaInvalidaError(
                "La duración debe ser un número mayor que cero."
            )

        self.cliente.validar()
        self.servicio.validar()

        return True

    def describir(self):
        """Devuelve la información completa de la reserva."""

        return (
            f"Reserva: {self.id} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} horas | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo:,.2f}"
        )

    def confirmar(self):
        """Confirma una reserva usando try/except/else."""

        try:
            if self.estado != "pendiente":
                raise ReservaInvalidaError(
                    "Solo se pueden confirmar reservas pendientes."
                )

            self.validar()

            if getattr(self.servicio, "disponible", True) is False:
                raise ServicioNoDisponibleError(
                    "El servicio seleccionado no está disponible."
                )

        except (
            ReservaInvalidaError,
            ServicioNoDisponibleError,
            ParametroFaltanteError
        ) as error:
            registrar_error(
                f"Error al confirmar reserva {self.id}: {error}"
            )
            raise

        else:
            self.estado = "confirmada"

            registrar_evento(
                f"Reserva confirmada correctamente. ID: {self.id}"
            )

            return True

    def cancelar(self):
        """Cancela una reserva usando try/except/finally."""

        try:
            if self.estado == "cancelada":
                raise ReservaInvalidaError(
                    "La reserva ya se encuentra cancelada."
                )

            self.estado = "cancelada"

            registrar_evento(
                f"Reserva cancelada correctamente. ID: {self.id}"
            )

            return True

        except ReservaInvalidaError as error:
            registrar_error(
                f"Error al cancelar reserva {self.id}: {error}"
            )
            raise

        finally:
            registrar_evento(
                f"Finalizó el proceso de cancelación de reserva {self.id}."
            )

    def procesar(self):
        """Calcula el costo de una reserva confirmada."""

        try:
            if self.estado != "confirmada":
                raise ReservaInvalidaError(
                    "Solo se pueden procesar reservas confirmadas."
                )

            self.validar()

            costo_calculado = self.servicio.calcular_costo(
                self.duracion
            )

            if (
                not isinstance(costo_calculado, (int, float))
                or isinstance(costo_calculado, bool)
                or not math.isfinite(costo_calculado)
                or costo_calculado < 0
            ):
                raise ReservaInvalidaError(
                    "El costo calculado de la reserva no es válido."
                )

            self.costo = costo_calculado

            registrar_evento(
                f"Reserva procesada correctamente. ID: {self.id}, "
                f"Costo: ${self.costo:,.2f}"
            )

            return self.costo

        except ReservaInvalidaError as error:
            registrar_error(
                f"Error al procesar reserva {self.id}: {error}"
            )
            raise

        except Exception as error:
            registrar_error(
                f"Error inesperado al procesar reserva {self.id}: {error}"
            )

            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error

    def __str__(self):
        """Devuelve la descripción de la reserva."""
        return self.describir()


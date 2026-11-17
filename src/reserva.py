"""
Archivo: src/reserva.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 4

Clase Reserva: integra cliente, servicio, duración y estado, y permite
confirmar (try/except/else), cancelar (try/except/finally) y procesar
(raise ... from) las reservas.
"""

import math  # Para verificar que los números sean finitos (math.isfinite)

from src.entidad import Entidad  # Clase de la que hereda Reserva
from src.excepciones import ReservaInvalidaError  # Error para reservas inválidas
from src.excepciones import ServicioNoDisponibleError  # Error si el servicio no está disponible
from src.excepciones import ParametroFaltanteError  # Error para datos obligatorios vacíos
from src.logger import registrar_evento  # Para registrar eventos en el log
from src.logger import registrar_error  # Para registrar errores en el log


class Reserva(Entidad):  # Reserva hereda de la clase abstracta Entidad
    """Representa una reserva realizada por un cliente."""

    def __init__(self, id_reserva, cliente, servicio, duracion):  # Constructor de la reserva
        """Crea la reserva en estado pendiente y valida sus datos."""
        super().__init__(id_reserva)  # Entidad guarda y valida el identificador

        self.cliente = cliente  # Guarda el cliente que hace la reserva
        self.servicio = servicio  # Guarda el servicio reservado
        self.duracion = duracion  # Guarda la duración en horas
        self.estado = "pendiente"  # Toda reserva nueva inicia como pendiente
        self.costo = 0  # El costo se calcula después, al procesar

        self.validar()  # Verifica los datos antes de terminar de crearla

        registrar_evento(  # Registra en el log la creación de la reserva
            f"Reserva creada correctamente. ID: {self.id}"  # Mensaje con el id de la reserva
        )

    def validar(self):  # Implementa el método abstracto de Entidad
        """Verifica que los datos de la reserva sean correctos."""

        from src.cliente import Cliente  # Importación local para evitar importaciones circulares
        from src.servicios import Servicio  # Importación local para evitar importaciones circulares

        if self.cliente is None:  # Si no se indicó un cliente
            raise ParametroFaltanteError(  # Lanza error por dato obligatorio faltante
                "Debe seleccionar un cliente para la reserva."  # Mensaje del error
            )

        if not isinstance(self.cliente, Cliente):  # Si el objeto no es un Cliente
            raise ReservaInvalidaError(  # Lanza error de reserva inválida
                "El cliente seleccionado no es válido."  # Mensaje del error
            )

        if self.servicio is None:  # Si no se indicó un servicio
            raise ParametroFaltanteError(  # Lanza error por dato obligatorio faltante
                "Debe seleccionar un servicio para la reserva."  # Mensaje del error
            )

        if not isinstance(self.servicio, Servicio):  # Si el objeto no es un Servicio
            raise ReservaInvalidaError(  # Lanza error de reserva inválida
                "El servicio seleccionado no es válido."  # Mensaje del error
            )

        if (  # La duración es inválida si se cumple alguna condición
            not isinstance(self.duracion, (int, float))  # No es un número
            or isinstance(self.duracion, bool)  # Es un booleano (True/False)
            or not math.isfinite(self.duracion)  # Es infinito o NaN
            or self.duracion <= 0  # Es cero o negativa
        ):
            raise ReservaInvalidaError(  # Lanza error de reserva inválida
                "La duración debe ser un número mayor que cero."  # Mensaje del error
            )

        self.cliente.validar()  # Valida también los datos del cliente
        self.servicio.validar()  # Valida también los datos del servicio

        return True  # Todos los datos son correctos

    def describir(self):  # Implementa el método abstracto de Entidad
        """Devuelve la información completa de la reserva."""

        return (  # Retorna un texto armado con varias partes
            f"Reserva: {self.id} | "  # Identificador de la reserva
            f"Cliente: {self.cliente.nombre} | "  # Nombre del cliente
            f"Servicio: {self.servicio.nombre} | "  # Nombre del servicio
            f"Duración: {self.duracion} horas | "  # Duración en horas
            f"Estado: {self.estado} | "  # Estado actual
            f"Costo: ${self.costo:,.2f}"  # Costo con separador de miles y 2 decimales
        )

    def confirmar(self):  # Pasa la reserva de pendiente a confirmada
        """Confirma una reserva usando try/except/else."""

        try:  # Bloque donde pueden ocurrir errores
            if self.estado != "pendiente":  # Solo se confirman reservas pendientes
                raise ReservaInvalidaError(  # Lanza error si no está pendiente
                    "Solo se pueden confirmar reservas pendientes."  # Mensaje del error
                )

            self.validar()  # Vuelve a validar los datos de la reserva

            if getattr(self.servicio, "disponible", True) is False:  # Si el servicio no está disponible
                raise ServicioNoDisponibleError(  # Lanza error de servicio no disponible
                    "El servicio seleccionado no está disponible."  # Mensaje del error
                )

        except (  # Captura cualquiera de estos errores
            ReservaInvalidaError,  # Reserva inválida
            ServicioNoDisponibleError,  # Servicio no disponible
            ParametroFaltanteError  # Dato obligatorio faltante
        ) as error:
            registrar_error(  # Registra el error en el log
                f"Error al confirmar reserva {self.id}: {error}"  # Mensaje con id y causa
            )
            raise  # Vuelve a lanzar el mismo error

        else:  # Se ejecuta solo si no hubo errores
            self.estado = "confirmada"  # Cambia el estado a confirmada

            registrar_evento(  # Registra la confirmación en el log
                f"Reserva confirmada correctamente. ID: {self.id}"  # Mensaje con el id
            )

            return True  # Indica que se confirmó correctamente

    def cancelar(self):  # Pasa la reserva a estado cancelada
        """Cancela una reserva usando try/except/finally."""

        try:  # Bloque donde pueden ocurrir errores
            if self.estado == "cancelada":  # Si ya estaba cancelada
                raise ReservaInvalidaError(  # Lanza error de reserva inválida
                    "La reserva ya se encuentra cancelada."  # Mensaje del error
                )

            self.estado = "cancelada"  # Cambia el estado a cancelada

            registrar_evento(  # Registra la cancelación en el log
                f"Reserva cancelada correctamente. ID: {self.id}"  # Mensaje con el id
            )

            return True  # Indica que se canceló correctamente

        except ReservaInvalidaError as error:  # Captura el error de reserva inválida
            registrar_error(  # Registra el error en el log
                f"Error al cancelar reserva {self.id}: {error}"  # Mensaje con id y causa
            )
            raise  # Vuelve a lanzar el mismo error

        finally:  # Se ejecuta siempre, haya o no error
            registrar_evento(  # Registra el fin del proceso en el log
                f"Finalizó el proceso de cancelación de reserva {self.id}."  # Mensaje con el id
            )

    def procesar(self):  # Calcula y guarda el costo de la reserva
        """Calcula el costo de una reserva confirmada."""

        try:  # Bloque donde pueden ocurrir errores
            if self.estado != "confirmada":  # Solo se procesan reservas confirmadas
                raise ReservaInvalidaError(  # Lanza error si no está confirmada
                    "Solo se pueden procesar reservas confirmadas."  # Mensaje del error
                )

            self.validar()  # Vuelve a validar los datos de la reserva

            costo_calculado = self.servicio.calcular_costo(  # Pide al servicio calcular el costo
                self.duracion  # Usa la duración de la reserva
            )

            if (  # El costo es inválido si se cumple alguna condición
                not isinstance(costo_calculado, (int, float))  # No es un número
                or isinstance(costo_calculado, bool)  # Es un booleano (True/False)
                or not math.isfinite(costo_calculado)  # Es infinito o NaN
                or costo_calculado < 0  # Es negativo
            ):
                raise ReservaInvalidaError(  # Lanza error de reserva inválida
                    "El costo calculado de la reserva no es válido."  # Mensaje del error
                )

            self.costo = costo_calculado  # Guarda el costo en la reserva

            registrar_evento(  # Registra el procesamiento en el log
                f"Reserva procesada correctamente. ID: {self.id}, "  # Mensaje con el id
                f"Costo: ${self.costo:,.2f}"  # y el costo con formato de moneda
            )

            return self.costo  # Devuelve el costo calculado

        except ReservaInvalidaError as error:  # Captura el error de reserva inválida
            registrar_error(  # Registra el error en el log
                f"Error al procesar reserva {self.id}: {error}"  # Mensaje con id y causa
            )
            raise  # Vuelve a lanzar el mismo error

        except Exception as error:  # Captura cualquier otro error inesperado
            registrar_error(  # Registra el error inesperado en el log
                f"Error inesperado al procesar reserva {self.id}: {error}"  # Mensaje con id y causa
            )

            raise ReservaInvalidaError(  # Lanza un error propio del sistema
                "No fue posible procesar la reserva."  # Mensaje del error
            ) from error  # Encadena el error original como causa

    def __str__(self):  # Representación en texto del objeto
        """Devuelve la descripción de la reserva."""
        return self.describir()  # Reutiliza el método describir

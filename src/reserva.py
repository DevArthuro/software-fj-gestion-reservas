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

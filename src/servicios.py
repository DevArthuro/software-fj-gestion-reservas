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

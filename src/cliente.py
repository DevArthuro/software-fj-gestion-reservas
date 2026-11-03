# ==========================================================
# Archivo: src/cliente.py
# ARCHIVO BASE PARA OTRO ESTUDIANTE – Responsable: Estudiante 2
#
# TODO: Crear la clase Cliente(Entidad) con atributos privados __nombre,
#       __documento, __correo y __telefono, cada uno con @property.
# TODO: Validar: correo con formato válido, documento numérico, campos no vacíos.
# TODO: Implementar describir() y validar().
# ==========================================================

from src.entidad import Entidad  # Clase abstracta de la que hereda Cliente
from src.excepciones import ClienteInvalidoError  # Error para datos de cliente inválidos
from src.excepciones import ParametroFaltanteError  # Error para datos obligatorios vacíos
from src.logger import registrar_evento  # Para registrar eventos en el log
from src.logger import registrar_error  # Para registrar errores en el log

"""Clase abstracta que representa cualquier entidad general del sistema."""

from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas

from src.excepciones import ParametroFaltanteError  # Error para cuando falta el identificador


class Entidad(ABC):
    """Clase abstracta base de Cliente, Servicio y Reserva."""

    def __init__(self, id_entidad):
        """Guarda el identificador de la entidad."""
        if not id_entidad:  # Si el id es None o está vacío
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")  # Lanza el error
        self._id = id_entidad  # Guarda el id en un atributo protegido

    @property
    def id(self):
        """Retorna el identificador (solo lectura)."""
        return self._id  # Devuelve el id guardado

    @abstractmethod
    def describir(self):
        """Retorna un texto que describe la entidad."""
        pass  # Las clases hijas deben implementarlo

    @abstractmethod
    def validar(self):
        """Valida los datos de la entidad y lanza una excepción si no son correctos."""
        pass  # Las clases hijas deben implementarlo

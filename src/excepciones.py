"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todas las excepciones del sistema."""

    def __init__(self, mensaje):
        """Guarda el mensaje del error."""
        super().__init__(mensaje)  # Llama al constructor de Exception con el mensaje
        self.mensaje = mensaje  # Guarda el mensaje para poder mostrarlo después

    def __str__(self):
        """Retorna el mensaje como texto."""
        return self.mensaje  # Devuelve el mensaje guardado


class ClienteInvalidoError(SoftwareFJError):
    """Se usa cuando los datos de un cliente son inválidos o el cliente está duplicado (Estudiante 2)."""

    pass  # No necesita nada más, hereda todo de la clase base


class ServicioInvalidoError(SoftwareFJError):
    """Se usa cuando los datos o parámetros de un servicio son inválidos (Estudiante 3)."""

    pass  # No necesita nada más, hereda todo de la clase base


class ServicioNoDisponibleError(SoftwareFJError):
    """Se usa cuando el servicio no está disponible para reservar (Estudiantes 3 y 4)."""

    pass  # No necesita nada más, hereda todo de la clase base


class ReservaInvalidaError(SoftwareFJError):
    """Se usa cuando una reserva es incorrecta o la operación sobre ella no está permitida (Estudiante 4)."""

    pass  # No necesita nada más, hereda todo de la clase base


class ParametroFaltanteError(SoftwareFJError):
    """Se usa cuando falta un dato obligatorio (todos los estudiantes)."""

    pass  # No necesita nada más, hereda todo de la clase base


class CalculoInconsistenteError(SoftwareFJError):
    """Se usa cuando un cálculo de costo da un resultado inválido, por ejemplo negativo (Estudiante 3)."""

    pass  # No necesita nada más, hereda todo de la clase base

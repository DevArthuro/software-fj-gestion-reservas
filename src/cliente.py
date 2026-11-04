"""
Archivo: src/cliente.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 2
Descripción: Clase Cliente para gestionar y validar la información
de los clientes del sistema.
"""

import re

from src.entidad import Entidad
from src.excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError
)
from src.logger import registrar_evento, registrar_error


class Cliente(Entidad):
    """Representa un cliente del sistema Software FJ."""

    def __init__(self, id_entidad, nombre, documento, correo, telefono):
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")

        if not documento or not str(documento).strip():
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")

        if not correo or not str(correo).strip():
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")

        if not telefono or not str(telefono).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")

        super().__init__(id_entidad)

        self.__nombre = str(nombre).strip()
        self.__documento = str(documento).strip()
        self.__correo = str(correo).strip()
        self.__telefono = str(telefono).strip()

        self.validar()
        registrar_evento(f"Cliente creado correctamente. ID: {self.id}")

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        nombre_anterior = self.__nombre
        self.__nombre = str(nuevo_nombre).strip()
        try:
            self.validar()
        except Exception:
            self.__nombre = nombre_anterior
            raise

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, nuevo_documento):
        documento_anterior = self.__documento
        self.__documento = str(nuevo_documento).strip()
        try:
            self.validar()
        except Exception:
            self.__documento = documento_anterior
            raise

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):
        correo_anterior = self.__correo
        self.__correo = str(nuevo_correo).strip()
        try:
            self.validar()
        except Exception:
            self.__correo = correo_anterior
            raise

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        telefono_anterior = self.__telefono
        self.__telefono = str(nuevo_telefono).strip()
        try:
            self.validar()
        except Exception:
            self.__telefono = telefono_anterior
            raise

    def validar(self):
        """Verifica que los datos del cliente sean correctos."""

        if not self.__nombre:
            raise ClienteInvalidoError(
                "El nombre del cliente no puede estar vacío."
            )

        if not self.__documento.isdigit():
            raise ClienteInvalidoError(
                "El documento debe contener únicamente números."
            )

        patron_correo = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.match(patron_correo, self.__correo):
            raise ClienteInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )

        if not self.__telefono.isdigit() or len(self.__telefono) != 10:
            raise ClienteInvalidoError(
                "El teléfono debe contener exactamente 10 dígitos numéricos."
            )

        return True

    def describir(self):
        """Devuelve la información completa del cliente."""

        return (
            f"ID: {self.id} | "
            f"Nombre: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )

    def __str__(self):
        return self.describir()
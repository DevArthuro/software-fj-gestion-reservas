"""
Archivo: src/cliente.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 2
Descripción: Clase Cliente para gestionar y validar la información
de los clientes del sistema.
"""

import re  # Permite usar expresiones regulares para validar el correo

from src.entidad import Entidad  # Clase abstracta base de la que hereda Cliente
from src.excepciones import (  # Importa las excepciones personalizadas que usa la clase
    ClienteInvalidoError,  # Error cuando los datos del cliente no son válidos
    ParametroFaltanteError  # Error cuando falta un dato obligatorio
)
from src.logger import registrar_evento, registrar_error  # Funciones para escribir en el log


class Cliente(Entidad):  # Define la clase Cliente, que hereda de Entidad
    """Representa un cliente del sistema Software FJ."""

    def __init__(self, id_entidad, nombre, documento, correo, telefono):  # Constructor con los datos del cliente
        """Crea el cliente, valida sus datos y registra el evento."""
        if not nombre or not str(nombre).strip():  # Si el nombre falta o solo tiene espacios
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")  # Lanza el error de dato faltante

        if not documento or not str(documento).strip():  # Si el documento falta o solo tiene espacios
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")  # Lanza el error de dato faltante

        if not correo or not str(correo).strip():  # Si el correo falta o solo tiene espacios
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")  # Lanza el error de dato faltante

        if not telefono or not str(telefono).strip():  # Si el teléfono falta o solo tiene espacios
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")  # Lanza el error de dato faltante

        super().__init__(id_entidad)  # Llama al constructor de Entidad para guardar el id

        self.__nombre = str(nombre).strip()  # Guarda el nombre sin espacios al inicio ni al final
        self.__documento = str(documento).strip()  # Guarda el documento sin espacios sobrantes
        self.__correo = str(correo).strip()  # Guarda el correo sin espacios sobrantes
        self.__telefono = str(telefono).strip()  # Guarda el teléfono sin espacios sobrantes

        self.validar()  # Revisa que los datos tengan el formato correcto
        registrar_evento(f"Cliente creado correctamente. ID: {self.id}")  # Registra la creación en el log

    @property
    def nombre(self):
        """Retorna el nombre del cliente."""
        return self.__nombre  # Devuelve el nombre guardado

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Cambia el nombre y lo restaura si no es válido."""
        nombre_anterior = self.__nombre  # Guarda el nombre actual por si hay que restaurarlo
        self.__nombre = str(nuevo_nombre).strip()  # Asigna el nuevo nombre sin espacios sobrantes
        try:  # Intenta validar el nuevo dato
            self.validar()  # Revisa que los datos sigan siendo correctos
        except Exception:  # Si la validación falla
            self.__nombre = nombre_anterior  # Restaura el nombre anterior
            raise  # Vuelve a lanzar el mismo error

    @property
    def documento(self):
        """Retorna el documento del cliente."""
        return self.__documento  # Devuelve el documento guardado

    @documento.setter
    def documento(self, nuevo_documento):
        """Cambia el documento y lo restaura si no es válido."""
        documento_anterior = self.__documento  # Guarda el documento actual por si hay que restaurarlo
        self.__documento = str(nuevo_documento).strip()  # Asigna el nuevo documento sin espacios sobrantes
        try:  # Intenta validar el nuevo dato
            self.validar()  # Revisa que los datos sigan siendo correctos
        except Exception:  # Si la validación falla
            self.__documento = documento_anterior  # Restaura el documento anterior
            raise  # Vuelve a lanzar el mismo error

    @property
    def correo(self):
        """Retorna el correo del cliente."""
        return self.__correo  # Devuelve el correo guardado

    @correo.setter
    def correo(self, nuevo_correo):
        """Cambia el correo y lo restaura si no es válido."""
        correo_anterior = self.__correo  # Guarda el correo actual por si hay que restaurarlo
        self.__correo = str(nuevo_correo).strip()  # Asigna el nuevo correo sin espacios sobrantes
        try:  # Intenta validar el nuevo dato
            self.validar()  # Revisa que los datos sigan siendo correctos
        except Exception:  # Si la validación falla
            self.__correo = correo_anterior  # Restaura el correo anterior
            raise  # Vuelve a lanzar el mismo error

    @property
    def telefono(self):
        """Retorna el teléfono del cliente."""
        return self.__telefono  # Devuelve el teléfono guardado

    @telefono.setter
    def telefono(self, nuevo_telefono):
        """Cambia el teléfono y lo restaura si no es válido."""
        telefono_anterior = self.__telefono  # Guarda el teléfono actual por si hay que restaurarlo
        self.__telefono = str(nuevo_telefono).strip()  # Asigna el nuevo teléfono sin espacios sobrantes
        try:  # Intenta validar el nuevo dato
            self.validar()  # Revisa que los datos sigan siendo correctos
        except Exception:  # Si la validación falla
            self.__telefono = telefono_anterior  # Restaura el teléfono anterior
            raise  # Vuelve a lanzar el mismo error

    def validar(self):
        """Verifica que los datos del cliente sean correctos."""

        if not self.__nombre:  # Si el nombre quedó vacío
            raise ClienteInvalidoError(  # Lanza el error de cliente inválido
                "El nombre del cliente no puede estar vacío."
            )

        if not self.__documento.isdigit():  # Si el documento tiene caracteres que no son números
            raise ClienteInvalidoError(  # Lanza el error de cliente inválido
                "El documento debe contener únicamente números."
            )

        patron_correo = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"  # Formato esperado: usuario@dominio.ext

        if not re.match(patron_correo, self.__correo):  # Si el correo no cumple el formato
            raise ClienteInvalidoError(  # Lanza el error de cliente inválido
                "El correo electrónico no tiene un formato válido."
            )

        if not self.__telefono.isdigit() or len(self.__telefono) != 10:  # Si el teléfono no es numérico o no tiene 10 dígitos
            raise ClienteInvalidoError(  # Lanza el error de cliente inválido
                "El teléfono debe contener exactamente 10 dígitos numéricos."
            )

        return True  # Todos los datos son válidos

    def describir(self):
        """Devuelve la información completa del cliente."""

        return (  # Retorna un solo texto armado con varias partes
            f"ID: {self.id} | "  # Identificador del cliente
            f"Nombre: {self.__nombre} | "  # Nombre del cliente
            f"Documento: {self.__documento} | "  # Documento del cliente
            f"Correo: {self.__correo} | "  # Correo del cliente
            f"Teléfono: {self.__telefono}"  # Teléfono del cliente
        )

    def __str__(self):
        """Retorna el cliente como texto legible."""
        return self.describir()  # Usa describir() para mostrar el cliente

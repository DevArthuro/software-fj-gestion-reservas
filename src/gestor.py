"""
Archivo: src/gestor.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 2 (Sección de clientes)

Administra las listas internas y las operaciones de clientes.
"""

from src.logger import registrar_evento, registrar_error
from src.cliente import Cliente
from src.servicios import Servicio
from src.excepciones import ServicioInvalidoError
from src.excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError
)


class Gestor:
    """Guarda y administra las listas del sistema."""

    def __init__(self):
        """Inicializa las listas de clientes, servicios y reservas."""

        self.clientes = []
        self.servicios = []
        self.reservas = []

        registrar_evento("Gestor creado con listas vacías.")

    # ==========================================================
    # SECCIÓN CLIENTES - RESPONSABLE: ESTUDIANTE 2
    # ==========================================================

    def registrar_cliente(self, cliente):
        """Valida y registra un nuevo cliente."""

        try:
            if cliente is None:
                raise ParametroFaltanteError(
                    "Debe proporcionar los datos del cliente."
                )

            if not isinstance(cliente, Cliente):
                raise ClienteInvalidoError(
                    "El objeto proporcionado no es un cliente válido."
                )

            cliente.validar()

            if self.buscar_cliente(cliente.documento) is not None:
                raise ClienteInvalidoError(
                    "Ya existe un cliente con ese documento."
                )

            self.clientes.append(cliente)

            registrar_evento(
                f"Cliente registrado correctamente. "
                f"ID: {cliente.id}, Documento: {cliente.documento}"
            )

            return cliente

        except (ParametroFaltanteError, ClienteInvalidoError) as error:
            registrar_error(f"Error al registrar cliente: {error}")
            raise

        except Exception as error:
            registrar_error(
                f"Error inesperado al registrar cliente: {error}"
            )
            raise ClienteInvalidoError(
                "No fue posible registrar el cliente."
            ) from error

        finally:
            registrar_evento(
                "Finalizó el proceso de registro de cliente."
            )

    def buscar_cliente(self, documento):
        """Busca un cliente por su número de documento."""

        try:
            if documento is None or not str(documento).strip():
                raise ParametroFaltanteError(
                    "Debe ingresar el documento del cliente."
                )

            documento = str(documento).strip()

            for cliente in self.clientes:
                if cliente.documento == documento:
                    registrar_evento(
                        f"Cliente encontrado. Documento: {documento}"
                    )
                    return cliente

            registrar_evento(
                f"No se encontró el cliente con documento: {documento}"
            )

            return None

        except ParametroFaltanteError as error:
            registrar_error(f"Error al buscar cliente: {error}")
            raise

        except Exception as error:
            registrar_error(
                f"Error inesperado al buscar cliente: {error}"
            )
            raise ClienteInvalidoError(
                "No fue posible realizar la búsqueda del cliente."
            ) from error

        finally:
            registrar_evento(
                "Finalizó el proceso de búsqueda de cliente."
            )

    def listar_clientes(self):
        """Devuelve una copia de los clientes registrados."""

        try:
            clientes_registrados = list(self.clientes)

            registrar_evento(
                f"Consulta de clientes realizada. "
                f"Total: {len(clientes_registrados)}"
            )

            return clientes_registrados

        except Exception as error:
            registrar_error(f"Error al listar clientes: {error}")
            raise ClienteInvalidoError(
                "No fue posible consultar los clientes registrados."
            ) from error

        finally:
            registrar_evento(
                "Finalizó el proceso de consulta de clientes."
            )

    def eliminar_cliente(self, documento):
        """Elimina un cliente utilizando su número de documento."""

        try:
            if documento is None or not str(documento).strip():
                raise ParametroFaltanteError(
                    "Debe proporcionar el documento del cliente."
                )

            documento = str(documento).strip()
            cliente = self.buscar_cliente(documento)

            if cliente is None:
                raise ClienteInvalidoError(
                    "No existe un cliente con ese documento."
                )

            self.clientes.remove(cliente)

            registrar_evento(
                f"Cliente eliminado. ID: {cliente.id}, "
                f"Documento: {cliente.documento}"
            )

            return cliente

        except (ParametroFaltanteError, ClienteInvalidoError) as error:
            registrar_error(f"Error al eliminar cliente: {error}")
            raise

        except Exception as error:
            registrar_error(
                f"Error inesperado al eliminar cliente: {error}"
            )
            raise ClienteInvalidoError(
                "No fue posible eliminar el cliente."
            ) from error

        finally:
            registrar_evento(
                "Finalizó el proceso de eliminación de cliente."
            )

    # ==========================================================
    # SECCIÓN SERVICIOS - RESPONSABLE: ESTUDIANTE 3
    # ==========================================================
    # El estudiante 3 implementará:
    # agregar_servicio()
    # listar_servicios()

    def agregar_servicio(self, servicio):
        """Valida y registra un nuevo servicio."""

        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError(
                "El objeto proporcionado no es un servicio válido."
            )

        servicio.validar_parametros()
        self.servicios.append(servicio)

        registrar_evento(
            f"Servicio registrado correctamente. ID: {servicio.id}"
        )

        return servicio

    def listar_servicios(self):
        """Devuelve una copia de los servicios registrados."""

        servicios_registrados = list(self.servicios)

        registrar_evento(
            f"Consulta de servicios realizada. "
            f"Total: {len(servicios_registrados)}"
        )

        return servicios_registrados


    # ==========================================================
    # SECCIÓN RESERVAS - RESPONSABLE: ESTUDIANTE 4
    # ==========================================================
    # El estudiante 4 implementará:
    # crear_reserva()
    # listar_reservas()
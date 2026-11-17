"""
Archivo: src/gestor.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsables: Estudiante 2 (clientes), Estudiante 3 (servicios) y Estudiante 4 (reservas)

Administra las listas internas del sistema (clientes, servicios y reservas)
sin usar bases de datos. Cada operación registra sus eventos y errores en el log.
"""

from src.logger import registrar_evento, registrar_error  # Funciones para escribir en el log
from src.cliente import Cliente  # Clase Cliente para validar el tipo de objeto
from src.servicios import Servicio  # Clase abstracta Servicio para validar el tipo de objeto
from src.reserva import Reserva  # Clase Reserva para validar el tipo de objeto
from src.excepciones import (  # Excepciones personalizadas que usa el gestor
    ClienteInvalidoError,  # Cliente inválido o duplicado
    ParametroFaltanteError,  # Falta un dato obligatorio
    ReservaInvalidaError,  # Reserva inválida o duplicada
    ServicioInvalidoError,  # Servicio inválido o duplicado
    ServicioNoDisponibleError,  # Servicio bloqueado para reservas
)


class Gestor:
    """Guarda y administra las listas del sistema."""

    def __init__(self):
        """Inicializa las listas de clientes, servicios y reservas."""
        self.clientes = []  # Lista interna de clientes
        self.servicios = []  # Lista interna de servicios
        self.reservas = []  # Lista interna de reservas
        registrar_evento("Gestor creado con listas vacías.")  # Deja constancia en el log

    # ==========================================================
    # SECCIÓN CLIENTES - RESPONSABLE: ESTUDIANTE 2
    # ==========================================================

    def registrar_cliente(self, cliente):
        """Valida y registra un nuevo cliente."""
        try:  # Intenta registrar el cliente
            if cliente is None:  # No se envió ningún cliente
                raise ParametroFaltanteError("Debe proporcionar los datos del cliente.")  # Falta el dato

            if not isinstance(cliente, Cliente):  # El objeto no es de la clase Cliente
                raise ClienteInvalidoError("El objeto proporcionado no es un cliente válido.")  # Tipo inválido

            cliente.validar()  # Revisa nombre, documento, correo y teléfono

            if self.buscar_cliente(cliente.documento) is not None:  # Ya hay un cliente con ese documento
                raise ClienteInvalidoError("Ya existe un cliente con ese documento.")  # Cliente duplicado

            self.clientes.append(cliente)  # Guarda el cliente en la lista
            registrar_evento(  # Deja constancia del registro
                f"Cliente registrado correctamente. ID: {cliente.id}, Documento: {cliente.documento}"
            )
            return cliente  # Devuelve el cliente registrado

        except (ParametroFaltanteError, ClienteInvalidoError) as error:  # Errores previstos
            registrar_error(f"Error al registrar cliente: {error}")  # Los guarda en el log
            raise  # Los vuelve a lanzar para que la interfaz los muestre

        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error inesperado al registrar cliente: {error}")  # Lo guarda en el log
            raise ClienteInvalidoError("No fue posible registrar el cliente.") from error  # Encadenamiento

        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de registro de cliente.")  # Cierre del proceso

    def buscar_cliente(self, documento):
        """Busca un cliente por su número de documento; retorna None si no existe."""
        try:  # Intenta buscar el cliente
            if documento is None or not str(documento).strip():  # El documento está vacío
                raise ParametroFaltanteError("Debe ingresar el documento del cliente.")  # Falta el dato

            documento = str(documento).strip()  # Limpia espacios del documento

            for cliente in self.clientes:  # Recorre la lista de clientes
                if cliente.documento == documento:  # Encontró el documento buscado
                    registrar_evento(f"Cliente encontrado. Documento: {documento}")  # Deja constancia
                    return cliente  # Devuelve el cliente encontrado

            registrar_evento(f"No se encontró el cliente con documento: {documento}")  # Búsqueda sin resultado
            return None  # No existe un cliente con ese documento

        except ParametroFaltanteError as error:  # Error previsto
            registrar_error(f"Error al buscar cliente: {error}")  # Lo guarda en el log
            raise  # Lo vuelve a lanzar

        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error inesperado al buscar cliente: {error}")  # Lo guarda en el log
            raise ClienteInvalidoError("No fue posible realizar la búsqueda del cliente.") from error  # Encadenamiento

        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de búsqueda de cliente.")  # Cierre del proceso

    def listar_clientes(self):
        """Devuelve una copia de los clientes registrados."""
        try:  # Intenta copiar la lista
            clientes_registrados = list(self.clientes)  # Copia para no exponer la lista interna
            registrar_evento(f"Consulta de clientes realizada. Total: {len(clientes_registrados)}")  # Deja constancia
            return clientes_registrados  # Devuelve la copia

        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error al listar clientes: {error}")  # Lo guarda en el log
            raise ClienteInvalidoError("No fue posible consultar los clientes registrados.") from error  # Encadenamiento

        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de consulta de clientes.")  # Cierre del proceso

    def eliminar_cliente(self, documento):
        """Elimina un cliente utilizando su número de documento."""
        try:  # Intenta eliminar el cliente
            if documento is None or not str(documento).strip():  # El documento está vacío
                raise ParametroFaltanteError("Debe proporcionar el documento del cliente.")  # Falta el dato

            documento = str(documento).strip()  # Limpia espacios del documento
            cliente = self.buscar_cliente(documento)  # Busca el cliente en la lista

            if cliente is None:  # No existe el cliente
                raise ClienteInvalidoError("No existe un cliente con ese documento.")  # Operación no permitida

            self.clientes.remove(cliente)  # Quita el cliente de la lista
            registrar_evento(  # Deja constancia de la eliminación
                f"Cliente eliminado. ID: {cliente.id}, Documento: {cliente.documento}"
            )
            return cliente  # Devuelve el cliente eliminado

        except (ParametroFaltanteError, ClienteInvalidoError) as error:  # Errores previstos
            registrar_error(f"Error al eliminar cliente: {error}")  # Los guarda en el log
            raise  # Los vuelve a lanzar

        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error inesperado al eliminar cliente: {error}")  # Lo guarda en el log
            raise ClienteInvalidoError("No fue posible eliminar el cliente.") from error  # Encadenamiento

        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de eliminación de cliente.")  # Cierre del proceso

    # ==========================================================
    # SECCIÓN SERVICIOS - RESPONSABLE: ESTUDIANTE 3
    # ==========================================================

    def agregar_servicio(self, servicio):
        """Valida y registra un nuevo servicio (try/except/else/finally)."""
        try:  # Intenta validar el servicio
            if not isinstance(servicio, Servicio):  # Debe ser una sala, un equipo o una asesoría
                raise ServicioInvalidoError("El objeto proporcionado no es un servicio válido.")  # Tipo inválido
            servicio.validar_parametros()  # Cada hija valida sus datos (polimorfismo)
            if any(existente.id == servicio.id for existente in self.servicios):  # ID repetido
                raise ServicioInvalidoError("Ya existe un servicio con ese identificador.")  # Servicio duplicado
        except (ServicioInvalidoError, ParametroFaltanteError) as error:  # Errores previstos
            registrar_error(f"Error al registrar servicio: {error}")  # Queda en el log
            raise  # Lo vuelve a lanzar para que la interfaz lo muestre
        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error inesperado al registrar servicio: {error}")  # Error no previsto
            raise ServicioInvalidoError("No fue posible registrar el servicio.") from error  # Encadenamiento
        else:  # Solo se ejecuta si no hubo errores
            self.servicios.append(servicio)  # Guarda el servicio en la lista
            registrar_evento(f"Servicio registrado correctamente. ID: {servicio.id}")  # Evento
            return servicio  # Devuelve el servicio registrado
        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de registro de servicio.")  # Cierre del proceso

    def buscar_servicio(self, id_servicio):
        """Busca un servicio por su identificador; retorna None si no existe."""
        for servicio in self.servicios:  # Recorre la lista de servicios
            if servicio.id == id_servicio:  # Encontró el ID buscado
                return servicio  # Devuelve el servicio encontrado
        return None  # No existe un servicio con ese ID

    def cambiar_disponibilidad_servicio(self, id_servicio, disponible):
        """Marca un servicio como disponible o no disponible (try/except/finally)."""
        try:  # Intenta cambiar la disponibilidad
            if id_servicio is None or not str(id_servicio).strip():  # El ID está vacío
                raise ParametroFaltanteError("Debe indicar el identificador del servicio.")  # Falta el dato
            servicio = self.buscar_servicio(str(id_servicio).strip())  # Busca el servicio por ID
            if servicio is None:  # No existe el servicio
                raise ServicioInvalidoError(f"No existe un servicio con el ID {id_servicio}.")  # Servicio inválido
            servicio.cambiar_disponibilidad(disponible)  # Cambia el estado en el servicio
            return servicio  # Devuelve el servicio actualizado
        except (ServicioInvalidoError, ParametroFaltanteError) as error:  # Errores previstos
            registrar_error(f"Error al cambiar disponibilidad del servicio: {error}")  # Queda en el log
            raise  # Lo vuelve a lanzar para que la interfaz lo muestre
        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el cambio de disponibilidad de servicio.")  # Cierre del proceso

    def listar_servicios(self):
        """Devuelve una copia de los servicios registrados."""
        servicios_registrados = list(self.servicios)  # Copia para no exponer la lista interna
        registrar_evento(f"Consulta de servicios realizada. Total: {len(servicios_registrados)}")  # Deja constancia
        return servicios_registrados  # Devuelve la copia

    # ==========================================================
    # SECCIÓN RESERVAS - RESPONSABLE: ESTUDIANTE 4
    # ==========================================================

    def crear_reserva(self, reserva):
        """Valida y registra una nueva reserva."""
        try:  # Intenta registrar la reserva
            if reserva is None:  # No se envió ninguna reserva
                raise ParametroFaltanteError("Debe proporcionar una reserva.")  # Falta el dato

            if not isinstance(reserva, Reserva):  # El objeto no es de la clase Reserva
                raise ReservaInvalidaError("El objeto proporcionado no es una reserva válida.")  # Tipo inválido

            reserva.validar()  # Revisa cliente, servicio y duración

            if any(existente.id == reserva.id for existente in self.reservas):  # ID repetido
                raise ReservaInvalidaError("Ya existe una reserva con ese identificador.")  # Reserva duplicada

            if reserva.cliente not in self.clientes:  # El cliente no está en el sistema
                raise ReservaInvalidaError("El cliente no está registrado en el sistema.")  # Reserva inválida

            if reserva.servicio not in self.servicios:  # El servicio no está en el sistema
                raise ReservaInvalidaError("El servicio no está registrado en el sistema.")  # Reserva inválida

            if not reserva.servicio.disponible:  # El servicio existe pero está bloqueado
                raise ServicioNoDisponibleError(
                    f"El servicio {reserva.servicio.nombre} no está disponible."  # Mensaje para el usuario
                )

            self.reservas.append(reserva)  # Guarda la reserva en la lista
            registrar_evento(f"Reserva registrada correctamente. ID: {reserva.id}")  # Deja constancia
            return reserva  # Devuelve la reserva registrada

        except (ParametroFaltanteError, ReservaInvalidaError, ServicioNoDisponibleError) as error:  # Errores previstos
            registrar_error(f"Error al crear reserva: {error}")  # Los guarda en el log
            raise  # Los vuelve a lanzar para que la interfaz los muestre

        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error inesperado al crear reserva: {error}")  # Lo guarda en el log
            raise ReservaInvalidaError("No fue posible registrar la reserva.") from error  # Encadenamiento

        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de creación de reserva.")  # Cierre del proceso

    def listar_reservas(self):
        """Devuelve una copia de las reservas registradas."""
        try:  # Intenta copiar la lista
            reservas_registradas = list(self.reservas)  # Copia para no exponer la lista interna
            registrar_evento(f"Consulta de reservas realizada. Total: {len(reservas_registradas)}")  # Deja constancia
            return reservas_registradas  # Devuelve la copia

        except Exception as error:  # Cualquier error no previsto
            registrar_error(f"Error al listar reservas: {error}")  # Lo guarda en el log
            raise ReservaInvalidaError("No fue posible consultar las reservas.") from error  # Encadenamiento

        finally:  # Se ejecuta siempre
            registrar_evento("Finalizó el proceso de consulta de reservas.")  # Cierre del proceso

"""Gestor que guarda todas las listas internas del sistema (reemplaza a la base de datos)."""

from src.logger import registrar_evento  # Para registrar la creación del gestor


class Gestor:
    """Guarda las listas de clientes, servicios y reservas."""

    def __init__(self):
        """Crea las tres listas vacías."""
        self.clientes = []  # Lista donde se guardarán los clientes
        self.servicios = []  # Lista donde se guardarán los servicios
        self.reservas = []  # Lista donde se guardarán las reservas
        registrar_evento("Gestor creado con listas vacías.")  # Deja constancia en el log

    # ==========================================================
    # SECCIÓN CLIENTES – La implementa el Estudiante 2
    # Métodos esperados: registrar_cliente, buscar_cliente, listar_clientes
    # ==========================================================

    # ==========================================================
    # SECCIÓN SERVICIOS – La implementa el Estudiante 3
    # Métodos esperados: agregar_servicio, listar_servicios
    # ==========================================================

    # ==========================================================
    # SECCIÓN RESERVAS – La implementa el Estudiante 4
    # Métodos esperados: crear_reserva, listar_reservas
    # ==========================================================

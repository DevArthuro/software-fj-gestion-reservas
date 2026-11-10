"""
Archivo: simulacion.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 5

Simula operaciones correctas e incorrectas de clientes,
servicios y reservas, registrando los resultados en el log.
"""

from src.gestor import Gestor
from src.cliente import Cliente
from src.servicios import ReservaSala, AlquilerEquipo, Asesoria
from src.reserva import Reserva
from src.logger import registrar_evento, registrar_error


def ejecutar_prueba(nombre, operacion):
    """Ejecuta una operación y captura su resultado o error."""
    try:
        resultado = operacion()
        print(f"[CORRECTO] {nombre}")
        registrar_evento(f"Simulación correcta: {nombre}")
        return resultado

    except Exception as error:
        print(f"[ERROR] {nombre}: {error}")
        registrar_error(f"Simulación fallida: {nombre}: {error}")
        return None


def ejecutar_simulacion():
    """Ejecuta las pruebas de los módulos del sistema."""

    print("\n========== SIMULACIÓN SOFTWARE FJ ==========\n")
    registrar_evento("Inicio de la simulación.")

    gestor = Gestor()
    datos = {}

    # PRUEBAS DE CLIENTES

    datos["cliente"] = ejecutar_prueba(
        "Registrar cliente válido",
        lambda: gestor.registrar_cliente(
            Cliente(
                "C001",
                "Carlos Pérez",
                "123456789",
                "carlos@gmail.com",
                "3001234567"
            )
        )
    )

    ejecutar_prueba(
        "Registrar cliente inválido",
        lambda: Cliente(
            "C002",
            "",
            "123456",
            "correo_invalido",
            "123"
        )
    )

    ejecutar_prueba(
        "Registrar cliente duplicado",
        lambda: gestor.registrar_cliente(
            Cliente(
                "C003",
                "Carlos Pérez duplicado",
                "123456789",
                "duplicado@gmail.com",
                "3101234567"
            )
        )
    )

    ejecutar_prueba(
        "Consultar clientes",
        lambda: gestor.listar_clientes()
    )

    # PRUEBAS DE SERVICIOS

    datos["sala"] = ejecutar_prueba(
        "Registrar servicio de reserva de sala",
        lambda: gestor.agregar_servicio(
            ReservaSala(
                "S001",
                "Sala de reuniones",
                50000,
                10
            )
        )
    )

    ejecutar_prueba(
        "Registrar servicio de alquiler de equipo",
        lambda: gestor.agregar_servicio(
            AlquilerEquipo(
                "S002",
                "Proyector",
                20000,
                "Audiovisual"
            )
        )
    )

    ejecutar_prueba(
        "Registrar servicio de asesoría",
        lambda: gestor.agregar_servicio(
            Asesoria(
                "S003",
                "Asesoría técnica",
                60000,
                "Tecnología"
            )
        )
    )

    ejecutar_prueba(
        "Registrar servicio inválido",
        lambda: gestor.agregar_servicio(None)
    )

    ejecutar_prueba(
        "Consultar servicios",
        lambda: gestor.listar_servicios()
    )

    # PRUEBAS DE RESERVAS

    def crear_reserva_valida():
        if datos["cliente"] is None or datos["sala"] is None:
            raise ValueError(
                "No se puede crear la reserva porque falta "
                "un cliente o servicio válido."
            )

        reserva = Reserva(
            "R001",
            datos["cliente"],
            datos["sala"],
            2
        )

        datos["reserva"] = gestor.crear_reserva(reserva)
        return datos["reserva"]

    ejecutar_prueba(
        "Crear reserva válida",
        crear_reserva_valida
    )

    ejecutar_prueba(
        "Confirmar reserva",
        lambda: datos["reserva"].confirmar()
        if datos.get("reserva") is not None
        else (_ for _ in ()).throw(
            ValueError("No existe una reserva válida para confirmar.")
        )
    )

    ejecutar_prueba(
        "Procesar reserva confirmada",
        lambda: datos["reserva"].procesar()
        if datos.get("reserva") is not None
        else (_ for _ in ()).throw(
            ValueError("No existe una reserva para procesar.")
        )
    )

    ejecutar_prueba(
        "Crear reserva con duración inválida",
        lambda: Reserva(
            "R002",
            datos["cliente"],
            datos["sala"],
            0
        )
    )

    ejecutar_prueba(
        "Registrar reserva duplicada",
        lambda: gestor.crear_reserva(
            Reserva(
                "R001",
                datos["cliente"],
                datos["sala"],
                1
            )
        )
    )

    ejecutar_prueba(
        "Consultar reservas",
        lambda: gestor.listar_reservas()
    )

    # RESUMEN

    print("\n========== RESUMEN ==========")
    print(f"Clientes registrados: {len(gestor.clientes)}")
    print(f"Servicios registrados: {len(gestor.servicios)}")
    print(f"Reservas registradas: {len(gestor.reservas)}")
    print("Los resultados detallados están en logs/sistema.log")
    print("\n========== FIN DE LA SIMULACIÓN ==========\n")

    registrar_evento("Finalizó la simulación.")


if __name__ == "__main__":
    ejecutar_simulacion()
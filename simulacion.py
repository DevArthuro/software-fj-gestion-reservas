"""
Archivo: simulacion.py
Proyecto: Software FJ - Sistema Integral de Gestión
Responsable: Estudiante 5

Simula 23 operaciones correctas e incorrectas de clientes, servicios y
reservas. Cada error se captura sin detener el programa y queda registrado
en logs/sistema.log. Se ejecuta con: python simulacion.py
"""

from src.gestor import Gestor  # Clase que guarda las listas del sistema
from src.cliente import Cliente  # Clase Cliente
from src.servicios import ReservaSala, AlquilerEquipo, Asesoria  # Servicios especializados
from src.reserva import Reserva  # Clase Reserva
from src.logger import registrar_evento, registrar_error  # Funciones para escribir en el log


def ejecutar_prueba(nombre, operacion, resumen=None):
    """Ejecuta una operación, muestra su resultado y captura cualquier error sin detener el programa."""
    if resumen is not None:  # Si se lleva el conteo de operaciones
        resumen["total"] += 1  # Suma una operación
    numero = resumen["total"] if resumen is not None else "-"  # Número de la operación para mostrarlo
    try:  # Intenta ejecutar la operación
        resultado = operacion()  # Ejecuta la función recibida
    except Exception as error:  # Cualquier error queda controlado aquí
        tipo = type(error).__name__  # Nombre de la excepción (ej.: ServicioInvalidoError)
        print(f"{numero:>2}. [ERROR] {nombre}: {tipo}: {error}")  # Muestra el tipo y el mensaje
        registrar_error(f"Simulación fallida: {nombre}: {tipo}: {error}")  # Lo guarda en el log
        if resumen is not None:  # Si se lleva el conteo
            resumen["errores"] += 1  # Suma un error controlado
            resumen["tipos"].add(tipo)  # Guarda el tipo de excepción
        return None  # No hay resultado
    else:  # Solo si no hubo errores
        print(f"{numero:>2}. [CORRECTO] {nombre}")  # Muestra que funcionó
        registrar_evento(f"Simulación correcta: {nombre}")  # Lo guarda en el log
        if resumen is not None:  # Si se lleva el conteo
            resumen["correctas"] += 1  # Suma una operación correcta
        return resultado  # Devuelve el resultado de la operación


def requerir(datos, clave):
    """Retorna un objeto creado en una operación anterior o lanza un error si esa operación falló."""
    if datos.get(clave) is None:  # La operación anterior no dejó el objeto
        raise ValueError(f"No existe '{clave}' porque una operación anterior falló.")  # Error controlado
    return datos[clave]  # Devuelve el objeto guardado


def ejecutar_simulacion():
    """Ejecuta las 23 operaciones de prueba de los módulos del sistema."""
    print("\n========== SIMULACIÓN SOFTWARE FJ ==========\n")  # Encabezado en consola
    registrar_evento("Inicio de la simulación.")  # Deja constancia del inicio

    gestor = Gestor()  # Gestor nuevo con listas vacías
    datos = {}  # Guarda los objetos creados para usarlos en otras operaciones
    resumen = {"total": 0, "correctas": 0, "errores": 0, "tipos": set()}  # Conteo de resultados

    # ---------------- CLIENTES ----------------
    print("--- Clientes ---")  # Subtítulo en consola
    datos["cliente"] = ejecutar_prueba(  # 1. Cliente válido
        "Registrar cliente válido",
        lambda: gestor.registrar_cliente(
            Cliente("C001", "Carlos Pérez", "123456789", "carlos@gmail.com", "3001234567")
        ),
        resumen,
    )
    ejecutar_prueba(  # 2. Cliente sin nombre -> ParametroFaltanteError
        "Registrar cliente inválido (sin nombre)",
        lambda: Cliente("C002", "", "123456", "correo_invalido", "123"),
        resumen,
    )
    ejecutar_prueba(  # 3. Documento repetido -> ClienteInvalidoError
        "Registrar cliente duplicado",
        lambda: gestor.registrar_cliente(
            Cliente("C003", "Carlos Pérez duplicado", "123456789", "duplicado@gmail.com", "3101234567")
        ),
        resumen,
    )
    ejecutar_prueba("Consultar clientes", gestor.listar_clientes, resumen)  # 4. Consulta

    # ---------------- SERVICIOS ----------------
    print("--- Servicios ---")  # Subtítulo en consola
    datos["sala"] = ejecutar_prueba(  # 5. Sala válida
        "Registrar servicio de reserva de sala",
        lambda: gestor.agregar_servicio(ReservaSala("S001", "Sala de reuniones", 50000, 10)),
        resumen,
    )
    ejecutar_prueba(  # 6. Equipo válido
        "Registrar servicio de alquiler de equipo",
        lambda: gestor.agregar_servicio(AlquilerEquipo("S002", "Proyector", 20000, "Audiovisual")),
        resumen,
    )
    datos["asesoria"] = ejecutar_prueba(  # 7. Asesoría válida
        "Registrar servicio de asesoría",
        lambda: gestor.agregar_servicio(Asesoria("S003", "Asesoría técnica", 60000, "Tecnología")),
        resumen,
    )
    ejecutar_prueba(  # 8. Objeto que no es servicio -> ServicioInvalidoError
        "Registrar servicio inválido (None)",
        lambda: gestor.agregar_servicio(None),
        resumen,
    )
    ejecutar_prueba(  # 9. Precio negativo -> ServicioInvalidoError
        "Registrar servicio con precio negativo",
        lambda: gestor.agregar_servicio(ReservaSala("S004", "Sala pequeña", -5000, 4)),
        resumen,
    )
    ejecutar_prueba(  # 10. ID repetido -> ServicioInvalidoError
        "Registrar servicio con ID repetido",
        lambda: gestor.agregar_servicio(AlquilerEquipo("S002", "Portátil", 15000, "Computador")),
        resumen,
    )
    datos["costo"] = ejecutar_prueba(  # 11. Sobrecarga: costo con impuesto y descuento
        "Calcular costo con impuesto (19%) y descuento (10%)",
        lambda: requerir(datos, "sala").calcular_costo(3, 19, 10),
        resumen,
    )
    ejecutar_prueba(  # 12. Descuento fuera de rango -> CalculoInconsistenteError
        "Calcular costo con descuento inválido (150%)",
        lambda: requerir(datos, "sala").calcular_costo(2, 19, 150),
        resumen,
    )
    ejecutar_prueba("Consultar servicios", gestor.listar_servicios, resumen)  # 13. Consulta

    # ---------------- RESERVAS ----------------
    print("--- Reservas ---")  # Subtítulo en consola
    datos["reserva"] = ejecutar_prueba(  # 14. Reserva válida
        "Crear reserva válida",
        lambda: gestor.crear_reserva(Reserva("R001", requerir(datos, "cliente"), requerir(datos, "sala"), 2)),
        resumen,
    )
    ejecutar_prueba(  # 15. try/except/else en Reserva.confirmar
        "Confirmar reserva",
        lambda: requerir(datos, "reserva").confirmar(),
        resumen,
    )
    ejecutar_prueba(  # 16. Cálculo del costo de la reserva confirmada
        "Procesar reserva confirmada",
        lambda: requerir(datos, "reserva").procesar(),
        resumen,
    )
    ejecutar_prueba(  # 17. Duración 0 -> ReservaInvalidaError
        "Crear reserva con duración inválida",
        lambda: Reserva("R002", requerir(datos, "cliente"), requerir(datos, "sala"), 0),
        resumen,
    )
    ejecutar_prueba(  # 18. ID repetido -> ReservaInvalidaError
        "Registrar reserva duplicada",
        lambda: gestor.crear_reserva(Reserva("R001", requerir(datos, "cliente"), requerir(datos, "sala"), 1)),
        resumen,
    )
    ejecutar_prueba(  # 19. Bloquea la asesoría
        "Marcar servicio S003 como no disponible",
        lambda: gestor.cambiar_disponibilidad_servicio("S003", False),
        resumen,
    )
    ejecutar_prueba(  # 20. Servicio bloqueado -> ServicioNoDisponibleError
        "Reservar un servicio no disponible",
        lambda: gestor.crear_reserva(
            Reserva("R003", requerir(datos, "cliente"), requerir(datos, "asesoria"), 1)
        ),
        resumen,
    )
    ejecutar_prueba(  # 21. try/except/finally en Reserva.cancelar
        "Cancelar reserva",
        lambda: requerir(datos, "reserva").cancelar(),
        resumen,
    )
    ejecutar_prueba(  # 22. Operación no permitida -> ReservaInvalidaError
        "Cancelar reserva ya cancelada",
        lambda: requerir(datos, "reserva").cancelar(),
        resumen,
    )
    ejecutar_prueba("Consultar reservas", gestor.listar_reservas, resumen)  # 23. Consulta

    # ---------------- RESUMEN ----------------
    print("\n========== RESUMEN ==========")  # Encabezado del resumen
    print(f"Operaciones ejecutadas: {resumen['total']}")  # Total de operaciones
    print(f"Correctas: {resumen['correctas']} | Errores controlados: {resumen['errores']}")  # Conteo
    print(f"Tipos de excepción manejados ({len(resumen['tipos'])}): {', '.join(sorted(resumen['tipos']))}")  # Tipos
    print(f"Clientes registrados: {len(gestor.clientes)}")  # Clientes en la lista
    print(f"Servicios registrados: {len(gestor.servicios)}")  # Servicios en la lista
    print(f"Reservas registradas: {len(gestor.reservas)}")  # Reservas en la lista
    print("Los resultados detallados están en logs/sistema.log")  # Dónde ver el detalle
    print("\n========== FIN DE LA SIMULACIÓN ==========\n")  # Cierre en consola

    registrar_evento(  # Deja constancia del fin con el conteo
        f"Finalizó la simulación: {resumen['total']} operaciones, "
        f"{resumen['correctas']} correctas y {resumen['errores']} errores controlados."
    )
    return resumen  # Devuelve el resumen (lo usa la pestaña Logs)


if __name__ == "__main__":  # Solo se ejecuta si se corre este archivo directamente
    ejecutar_simulacion()  # Inicia la simulación

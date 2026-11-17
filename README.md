# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la UNAD, curso Programación 213023, Fase 4 (Ejercicio 1 del Anexo 3).
Está hecho en Python con Programación Orientada a Objetos, Tkinter y manejo avanzado de excepciones.
No usa bases de datos: todo se guarda en listas de objetos y solo se escribe un archivo de log
(`logs/sistema.log`) con los eventos y errores.

## Requisitos

- Python 3.10 o superior **con Tkinter** (viene incluido en el instalador de python.org).
- No se necesita instalar nada con `pip`.

> En macOS, si `python -c "import tkinter"` falla (por ejemplo con Python de pyenv),
> use el instalador de python.org o `uv run --python 3.12 python main.py`.

## Cómo ejecutar

```
python main.py          # Abre la interfaz gráfica (pestañas Clientes, Servicios, Reservas y Logs)
python simulacion.py    # Ejecuta la simulación de 23 operaciones en consola
```

Resultado esperado de la simulación: **23 operaciones, 13 correctas y 10 errores controlados**,
con los 6 tipos de excepción del sistema. El programa nunca se detiene.

## Estructura de carpetas

```
software-fj-gestion-reservas/
├── README.md
├── .gitignore
├── main.py                       # Punto de entrada de la interfaz gráfica
├── simulacion.py                 # Simulación de 23 operaciones
├── logs/
│   └── .gitkeep                  # sistema.log se genera al ejecutar (no se sube al repositorio)
└── src/
    ├── __init__.py
    ├── excepciones.py            # 6 excepciones personalizadas + clase base
    ├── logger.py                 # Registro de eventos y errores
    ├── entidad.py                # Clase abstracta Entidad
    ├── gestor.py                 # Listas internas y operaciones del sistema
    ├── cliente.py                # Clase Cliente (encapsulación y validaciones)
    ├── servicios.py              # Clase abstracta Servicio y sus 3 hijas
    ├── reserva.py                # Clase Reserva (confirmar, cancelar, procesar)
    └── interfaz/
        ├── __init__.py
        ├── ventana_principal.py  # Ventana con pestañas
        ├── utilidades_gui.py     # Mensajes de error e información
        ├── pestana_clientes.py
        ├── pestana_servicios.py
        ├── pestana_reservas.py
        └── pestana_logs.py
```

## Diseño orientado a objetos

| Requisito del Anexo 3 | Dónde está |
|---|---|
| Clase abstracta de entidades generales | `Entidad` (`src/entidad.py`): `describir()` y `validar()` abstractos |
| Cliente con validaciones y encapsulación | `Cliente` (`src/cliente.py`): atributos privados `__nombre`, `__documento`… con propiedades y setters que validan |
| Clase abstracta Servicio + 3 servicios | `Servicio` (abstracta: `calcular_costo()` y `validar_parametros()`), `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| Polimorfismo y métodos sobrescritos | Cada hija sobrescribe `calcular_costo()`, `describir()` y `validar_parametros()` |
| Métodos sobrecargados | `calcular_costo(horas, impuesto=0, descuento=0)`: se puede llamar con 1, 2 o 3 argumentos |
| Reserva con cliente, servicio, duración y estado | `Reserva` (`src/reserva.py`): `confirmar()`, `cancelar()` y `procesar()` |
| Servicios no disponibles | `Servicio.disponible` y `Gestor.cambiar_disponibilidad_servicio()`; reservar uno bloqueado lanza `ServicioNoDisponibleError` |
| Listas internas, sin base de datos | `Gestor.clientes`, `Gestor.servicios`, `Gestor.reservas` |
| Archivo de logs | `src/logger.py` → `logs/sistema.log` |

## Manejo de excepciones

| Técnica | Dónde se usa |
|---|---|
| Excepciones personalizadas | `src/excepciones.py`: `SoftwareFJError` (base), `ClienteInvalidoError`, `ServicioInvalidoError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `ParametroFaltanteError`, `CalculoInconsistenteError` |
| `try / except` | Todas las pestañas de la interfaz y `simulacion.ejecutar_prueba()` |
| `try / except / else` | `Reserva.confirmar()`, `Gestor.agregar_servicio()`, `simulacion.ejecutar_prueba()` y las acciones de la pestaña Reservas |
| `try / except / finally` | `Reserva.cancelar()`, `Gestor.registrar_cliente()`, `buscar_cliente()`, `eliminar_cliente()`, `agregar_servicio()`, `cambiar_disponibilidad_servicio()`, `crear_reserva()`, `listar_reservas()` y `main.py` |
| Encadenamiento (`raise ... from`) | `Gestor` (errores inesperados), `Reserva.procesar()`, conversión de capacidad en la pestaña Servicios y de duración en la pestaña Reservas |
| Registro en el log | Cada error del modelo y de las 3 pestañas se escribe con `registrar_error()`; los eventos correctos con `registrar_evento()` |

## Integrantes y responsabilidades

| Estudiante | Nombre | Parte |
|---|---|---|
| 1 | Carlos Orrego | Base: excepciones, logger, clase abstracta Entidad, Gestor, ventana principal, utilidades de interfaz, main.py, README, correcciones finales |
| 2 | Naicy Mariana Mosquera Rivas | Clase Cliente + pestaña Clientes |
| 3 | Jose Narvaez | Clase Servicio y sus 3 hijas + pestaña Servicios |
| 4 | _(por completar)_ | Clase Reserva + pestaña Reservas |
| 5 | _(por completar)_ | Simulación de operaciones + pestaña Logs + documento final |

## Flujo de trabajo (ramas usadas)

Cada parte se desarrolló en su propia rama y se integró a `main` con un Pull Request:

- `feature/base` – estructura base del proyecto
- `Maraian-modulo-clientes` – módulo de clientes
- `feature/servicios` – módulo de servicios
- `feature/reservas` – módulo de reservas
- `feature/simulacion-logs` – simulación y pestaña de logs
- `fix/correcciones-entrega` – correcciones finales: `Servicio` abstracta, disponibilidad de servicios,
  `agregar_servicio()` robusto, todos los errores de la interfaz al log, simulación de 23 operaciones,
  limpieza y comentarios por línea

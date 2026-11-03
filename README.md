# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la UNAD, curso Programación 213023, Fase 4.
Está hecho en Python con Programación Orientada a Objetos, Tkinter y manejo de excepciones.
No usa bases de datos: todo se guarda en listas de objetos y solo se escribe un archivo de log.

## Requisitos

- Python 3.10 o superior (Tkinter viene incluido con Python).
- No se necesita instalar nada con `pip`.

## Cómo ejecutar

```
python main.py          # Abre la interfaz gráfica
python simulacion.py    # Ejecuta la simulación de operaciones
```

## Estructura de carpetas

```
software-fj-gestion-reservas/
├── README.md
├── .gitignore
├── main.py
├── simulacion.py                 # Simulación de 10 operaciones
├── logs/
│   └── .gitkeep
└── src/
    ├── __init__.py
    ├── excepciones.py            # Excepciones personalizadas
    ├── logger.py                 # Registro de eventos y errores
    ├── entidad.py                # Clase abstracta Entidad
    ├── gestor.py                 # Listas internas del sistema
    ├── cliente.py                # Clase Cliente
    ├── servicios.py              # Clase Servicio y sus hijas
    ├── reserva.py                # Clase Reserva
    └── interfaz/
        ├── __init__.py
        ├── ventana_principal.py  # Ventana con pestañas
        ├── utilidades_gui.py     # Mensajes de error e información
        ├── pestana_clientes.py
        ├── pestana_servicios.py
        ├── pestana_reservas.py
        └── pestana_logs.py
```

## Integrantes y responsabilidades

| Estudiante | Nombre | Parte |
|---|---|---|
| 1 | Nombre 1 | Base: excepciones, logger, clase abstracta Entidad, Gestor vacío, ventana principal, utilidades de interfaz, main.py, README |
| 2 | Nombre 2 | Clase Cliente + pestaña Clientes |
| 3 | Nombre 3 | Clase Servicio y sus 3 hijas + pestaña Servicios |
| 4 | Nombre 4 | Clase Reserva + pestaña Reservas |
| 5 | Nombre 5 | Simulación de 10 operaciones + pestaña Logs + documento final |

## Flujo de trabajo

Cada integrante trabaja en su propia rama y, al terminar, hace un Pull Request hacia `main`:

- `feature/base`
- `feature/clientes`
- `feature/servicios`
- `feature/reservas`
- `feature/simulacion`

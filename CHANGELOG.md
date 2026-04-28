# Changelog

Todas las novedades y cambios notables de este proyecto se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-28

### Añadido
- Documentación detallada de instalación y configuración para Windows (PowerShell y CMD), Linux y macOS en el `README.md`.
- Soporte para autenticación mediante token (OAuth) en la conexión a Snowflake.
- Ejemplos de consultas SQL avanzadas en `query_examples.md` y archivos SQL de entrada de ejemplo (`score_distribution.sql`, `rule_performance.sql`, `risk_factors.sql`).
- Archivo `CHANGELOG.md` para el seguimiento de versiones.

### Cambiado
- Estructura del `README.md` mejorada con tablas de parámetros y variables de entorno.
- El script `main.py` ahora prioriza el uso de tokens si están presentes.

## [1.0.0] - 2026-04-28

### Añadido
- Versión inicial del script exportador de consultas de Snowflake.
- Soporte para exportación en formatos CSV, Excel y TXT.
- Reemplazo dinámico de tokens `{data_from}` y `{date_end}`.
- Pruebas unitarias básicas en `test_main.py`.

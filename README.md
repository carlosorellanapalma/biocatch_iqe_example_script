# Snowflake Query Exporter

Este script permite ejecutar consultas SQL en Snowflake reemplazando tokens de fecha y exportando los resultados a diferentes formatos (CSV, Excel, TXT).

## Requisitos

- **Python 3.10+**
- Una cuenta activa de **Snowflake**.
- Dependencias de Python (ver sección de instalación).

## Instalación

1. **Clonar o descargar el repositorio.**

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

El script utiliza variables de entorno para la conexión a Snowflake. Puedes configurar estas variables creando un archivo `.env` en la raíz del proyecto.

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` con tus credenciales:

| Variable | Descripción |
| :--- | :--- |
| `SNOWFLAKE_USER` | Nombre de usuario de Snowflake. |
| `SNOWFLAKE_PASSWORD` | Contraseña del usuario. |
| `SNOWFLAKE_TOKEN` | Token de autenticación (OAuth) opcional. |
| `SNOWFLAKE_ACCOUNT` | Identificador de la cuenta (ej. `xy12345.east-us-2.azure`). |
| `SNOWFLAKE_WAREHOUSE` | Nombre del Virtual Warehouse a utilizar. |
| `SNOWFLAKE_DATABASE` | Base de datos por defecto. |
| `SNOWFLAKE_SCHEMA` | Esquema por defecto. |
| `SNOWFLAKE_ROLE` | Rol del usuario para la sesión. |

## Uso

Ejecuta el script utilizando `python main.py` seguido de los argumentos necesarios.

### Parámetros

| Parámetro | Requerido | Descripción | Valores permitidos | Predeterminado |
| :--- | :---: | :--- | :--- | :--- |
| `--input_file` | Sí | Ruta al archivo `.sql` que contiene la consulta. | Ruta de archivo | - |
| `--date_from` | Sí | Fecha que reemplazará el token `{data_from}`. | Texto (ej. YYYY-MM-DD) | - |
| `--date_end` | Sí | Fecha que reemplazará el token `{date_end}`. | Texto (ej. YYYY-MM-DD) | - |
| `--output_type` | Sí | Formato del archivo de salida. | `csv`, `excel`, `txt` | - |
| `--output_file` | No | Nombre base del archivo de salida (sin extensión). | Texto | `output` |
| `--token` | No | Token de autenticación (OAuth) para Snowflake. | Texto | - |

### Ejemplos de ejecución

**1. Exportar a CSV con tokens de fecha:**
```bash
python main.py --input_file query.sql --date_from 2024-01-01 --date_end 2024-01-31 --output_type csv
```

**2. Exportar a Excel con nombre de archivo personalizado:**
```bash
python main.py --input_file query.sql --date_from 2023-06-01 --date_end 2023-06-30 --output_type excel --output_file reporte_ventas_junio
```

**3. Exportar a TXT (Delimitado por tabulaciones):**
```bash
python main.py --input_file query.sql --date_from 2024-04-01 --date_end 2024-04-15 --output_type txt --output_file extracto_datos
```

**4. Conexión usando un Token (OAuth):**
```bash
python main.py --input_file query.sql --date_from 2024-01-01 --date_end 2024-01-31 --output_type csv --token "mi_token_oauth_aqui"
```

### Formato del Query SQL

El archivo SQL de entrada puede contener los tokens `{data_from}` y `{date_end}`, los cuales serán reemplazados dinámicamente por los valores pasados en los argumentos.

Para ver más ejemplos de consultas complejas (distribución de scores, métricas de reglas, etc.), consulta el archivo [query_examples.md](query_examples.md).

Ejemplo (`query.sql`):
```sql
SELECT * 
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS 
WHERE O_ORDERDATE BETWEEN '{data_from}' AND '{date_end}'
LIMIT 100;
```

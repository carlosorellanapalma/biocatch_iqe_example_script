# Snowflake Query Exporter

**Versión:** 1.1.0

Este script permite ejecutar consultas SQL en Snowflake reemplazando tokens de fecha y exportando los resultados a diferentes formatos (CSV, Excel, TXT).

## Requisitos

- **Python 3.10+**
- Una cuenta activa de **Snowflake**.
- Dependencias de Python (ver sección de instalación).

## Instalación y Configuración

A continuación se detallan los pasos para configurar el proyecto en diferentes sistemas operativos.

### Requisitos Previos
- **Python 3.10 o superior** instalado.
- **Git** (opcional, para clonar el repositorio).

---

###  macOS / 🐧 Linux

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/biocatchltd/biocatch_iqe_example_script.git
   cd biocatch_iqe_example_script
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (Temporal):**
   ```bash
   export SNOWFLAKE_USER="tu_usuario"
   export SNOWFLAKE_PASSWORD="tu_contraseña"
   # ... y así con el resto
   ```

---

### ⊞ Windows

#### Usando PowerShell (Recomendado)

1. **Clonar el repositorio:**
   ```powershell
   git clone https://github.com/biocatchltd/biocatch_iqe_example_script.git
   cd biocatch_iqe_example_script
   ```

2. **Crear y activar el entorno virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   *Nota: Si recibes un error de ejecución de scripts, ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.*

3. **Instalar dependencias:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (Temporal):**
   ```powershell
   $env:SNOWFLAKE_USER="tu_usuario"
   $env:SNOWFLAKE_PASSWORD="tu_contraseña"
   ```

#### Usando Símbolo del Sistema (CMD)

1. **Crear y activar el entorno virtual:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

2. **Configurar variables de entorno (Temporal):**
   ```cmd
   set SNOWFLAKE_USER=tu_usuario
   set SNOWFLAKE_PASSWORD=tu_contraseña
   ```

---

## Configuración Permanente (.env)

Independientemente del sistema operativo, puedes usar un archivo `.env` para no tener que configurar las variables en cada sesión.

1. Copia el archivo de ejemplo:
   - **macOS / Linux / PowerShell:** `cp .env.example .env`
   - **Windows (CMD):** `copy .env.example .env`

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

---
**Autor:** [Carlos Orellana Palma](https://github.com/carlosorellanapalma)

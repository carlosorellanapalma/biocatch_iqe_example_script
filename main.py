import os
import argparse
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import sys

def connect_to_snowflake(args=None):
    """Establece la conexión a Snowflake utilizando variables de entorno y/o parámetros."""
    try:
        # Prioridad: Argumento de línea de comandos > Variable de entorno
        token = args.token if args and args.token else os.getenv('SNOWFLAKE_TOKEN')
        user = os.getenv('SNOWFLAKE_USER')
        password = os.getenv('SNOWFLAKE_PASSWORD')
        account = os.getenv('SNOWFLAKE_ACCOUNT')
        warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        database = os.getenv('SNOWFLAKE_DATABASE')
        schema = os.getenv('SNOWFLAKE_SCHEMA')
        role = os.getenv('SNOWFLAKE_ROLE')

        conn_params = {
            'user': user,
            'account': account,
            'warehouse': warehouse,
            'database': database,
            'schema': schema,
            'role': role
        }

        if token:
            conn_params['authenticator'] = 'oauth'
            conn_params['token'] = token
        else:
            conn_params['password'] = password

        conn = snowflake.connector.connect(**conn_params)
        return conn
    except Exception as e:
        print(f"Error al conectar a Snowflake: {e}")
        sys.exit(1)

def main():
    # Cargar variables de entorno desde .env si existe
    load_dotenv()

    parser = argparse.ArgumentParser(description='Ejecuta un query en Snowflake y guarda el resultado.')
    parser.add_argument('--input_file', required=True, help='Archivo de entrada con el query SQL.')
    parser.add_argument('--date_from', required=True, help='Fecha de inicio (reemplaza {data_from}).')
    parser.add_argument('--date_end', required=True, help='Fecha de término (reemplaza {date_end}).')
    parser.add_argument('--output_type', required=True, choices=['txt', 'csv', 'excel'], help='Tipo de archivo de salida.')
    parser.add_argument('--output_file', default='output', help='Nombre base del archivo de salida (sin extensión).')
    parser.add_argument('--token', help='Token de autenticación (OAuth) para Snowflake.')

    args = parser.parse_args()

    # Leer el archivo de entrada
    try:
        with open(args.input_file, 'r') as f:
            query = f.read()
    except Exception as e:
        print(f"Error al leer el archivo de entrada: {e}")
        sys.exit(1)

    # Reemplazar tokens
    query = query.replace('{data_from}', args.date_from)
    query = query.replace('{date_end}', args.date_end)

    print(f"Ejecutando query en Snowflake...")
    
    # Conectar y ejecutar
    conn = connect_to_snowflake(args)
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error al ejecutar el query: {e}")
        conn.close()
        sys.exit(1)
    finally:
        conn.close()

    # Guardar resultado
    output_filename = f"{args.output_file}.{args.output_type if args.output_type != 'excel' else 'xlsx'}"
    
    try:
        if args.output_type == 'csv':
            df.to_csv(output_filename, index=False)
        elif args.output_type == 'excel':
            df.to_excel(output_filename, index=False)
        elif args.output_type == 'txt':
            # Para txt, podemos guardarlo como CSV con separador de tabulación o espacio
            df.to_csv(output_filename, sep='\t', index=False)
        
        print(f"Resultado guardado exitosamente en: {output_filename}")
    except Exception as e:
        print(f"Error al guardar el archivo de salida: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

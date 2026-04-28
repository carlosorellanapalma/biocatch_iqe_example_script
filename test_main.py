import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
import sys
from io import StringIO

# Importar la función main y otras necesarias de main
from main import main

class TestSnowflakeScript(unittest.TestCase):
    
    def setUp(self):
        # Crear un archivo de query de prueba
        with open('test_query.sql', 'w') as f:
            f.write("SELECT * FROM table WHERE date BETWEEN '{data_from}' AND '{date_end}'")
        
        # Configurar variables de entorno ficticias
        os.environ['SNOWFLAKE_USER'] = 'test_user'
        os.environ['SNOWFLAKE_PASSWORD'] = 'test_password'
        os.environ['SNOWFLAKE_ACCOUNT'] = 'test_account'
        os.environ['SNOWFLAKE_WAREHOUSE'] = 'test_warehouse'
        os.environ['SNOWFLAKE_DATABASE'] = 'test_db'
        os.environ['SNOWFLAKE_SCHEMA'] = 'test_schema'
        os.environ['SNOWFLAKE_ROLE'] = 'test_role'

    def tearDown(self):
        # Limpiar archivos creados
        files_to_remove = ['test_query.sql', 'test_output.csv', 'test_output.xlsx', 'test_output.txt']
        for f in files_to_remove:
            if os.path.exists(f):
                os.remove(f)

    @patch('snowflake.connector.connect')
    @patch('pandas.read_sql')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_flow_csv(self, mock_args, mock_read_sql, mock_connect):
        # Configurar mocks
        mock_args.return_value = MagicMock(
            input_file='test_query.sql',
            date_from='2023-01-01',
            date_end='2023-01-31',
            output_type='csv',
            output_file='test_output',
            token=None
        )
        
        # Simular DataFrame de retorno
        df_mock = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        mock_read_sql.return_value = df_mock
        
        # Ejecutar main
        main()
        
        # Verificar que se llamó a connect con los parámetros correctos
        mock_connect.assert_called_once()
        kwargs = mock_connect.call_args.kwargs
        self.assertEqual(kwargs['user'], 'test_user')
        self.assertEqual(kwargs['account'], 'test_account')
        self.assertIn('password', kwargs)
        self.assertEqual(kwargs['password'], 'test_password')
        
        # Verificar que se llamó a read_sql con el query procesado
        expected_query = "SELECT * FROM table WHERE date BETWEEN '2023-01-01' AND '2023-01-31'"
        mock_read_sql.assert_called_once()
        self.assertEqual(mock_read_sql.call_args[0][0], expected_query)
        
        # Verificar que se creó el archivo de salida
        self.assertTrue(os.path.exists('test_output.csv'))
        
        # Verificar contenido del archivo
        df_result = pd.read_csv('test_output.csv')
        self.assertEqual(len(df_result), 2)

    @patch('snowflake.connector.connect')
    @patch('pandas.read_sql')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_flow_excel(self, mock_args, mock_read_sql, mock_connect):
        # Configurar mocks
        mock_args.return_value = MagicMock(
            input_file='test_query.sql',
            date_from='2023-01-01',
            date_end='2023-01-31',
            output_type='excel',
            output_file='test_output',
            token=None
        )
        
        mock_read_sql.return_value = pd.DataFrame({'col1': [1]})
        
        # Ejecutar main
        main()
        
        # Verificar que se creó el archivo xlsx
        self.assertTrue(os.path.exists('test_output.xlsx'))

    @patch('snowflake.connector.connect')
    @patch('pandas.read_sql')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_flow_token(self, mock_args, mock_read_sql, mock_connect):
        # Configurar mocks con token
        mock_args.return_value = MagicMock(
            input_file='test_query.sql',
            date_from='2023-01-01',
            date_end='2023-01-31',
            output_type='csv',
            output_file='test_output',
            token='test_oauth_token'
        )
        
        mock_read_sql.return_value = pd.DataFrame({'col1': [1]})
        
        # Ejecutar main
        main()
        
        # Verificar parámetros de conexión para OAuth
        mock_connect.assert_called_once()
        kwargs = mock_connect.call_args.kwargs
        self.assertEqual(kwargs['authenticator'], 'oauth')
        self.assertEqual(kwargs['token'], 'test_oauth_token')
        self.assertNotIn('password', kwargs)

    @patch('snowflake.connector.connect')
    @patch('pandas.read_sql')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_flow_env_token(self, mock_args, mock_read_sql, mock_connect):
        # Configurar variable de entorno para token
        os.environ['SNOWFLAKE_TOKEN'] = 'env_oauth_token'
        
        # Mock de argumentos SIN token
        mock_args.return_value = MagicMock(
            input_file='test_query.sql',
            date_from='2023-01-01',
            date_end='2023-01-31',
            output_type='csv',
            output_file='test_output',
            token=None
        )
        
        mock_read_sql.return_value = pd.DataFrame({'col1': [1]})
        
        # Ejecutar main
        main()
        
        # Verificar que se usó el token de la variable de entorno
        kwargs = mock_connect.call_args.kwargs
        self.assertEqual(kwargs['authenticator'], 'oauth')
        self.assertEqual(kwargs['token'], 'env_oauth_token')
        
        # Limpiar env
        del os.environ['SNOWFLAKE_TOKEN']

if __name__ == '__main__':
    unittest.main()

import io
import os
import argparse
from zipfile import ZipFile
from boto3.session import Session
from dotenv import load_dotenv
import botocore.exceptions

# Cargar variables del archivo .env
load_dotenv()


def files_to_zip(path):
    for root, dirs, files in os.walk(path):
        # Omitir carpetas que terminan en '.dist-info'
        dirs[:] = [d for d in dirs if not d.endswith('.dist-info')]
        for f in files:
            full_path = os.path.join(root, f)
            archive_name = full_path[len(path) + len(os.sep):]
            yield full_path, archive_name


def make_zip_file_bytes(path):
    buf = io.BytesIO()
    with ZipFile(buf, 'w') as z:
        for full_path, archive_name in files_to_zip(path=path):
            z.write(full_path, archive_name)
    return buf.getvalue()


def update_lambda(lambda_name, lambda_code_path):
    try:
        # Obtener las credenciales y región de las variables de entorno
        aws_access_key = os.getenv('AWS_ACCESS_KEY')
        aws_secret_key = os.getenv('AWS_SECRET_KEY')
        region = os.getenv('AWS_REGION')

        # Crear la sesión de AWS
        session = Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        aws_lambda = session.client('lambda')

        # Verificar si el directorio existe
        if not os.path.isdir(lambda_code_path):
            raise ValueError(f'El directorio de Lambda no existe: {lambda_code_path}')

        # Crear archivo ZIP
        zip_bytes = make_zip_file_bytes(path=lambda_code_path)

        # Subir archivo ZIP a AWS Lambda
        response = aws_lambda.update_function_code(
            FunctionName=lambda_name,
            ZipFile=zip_bytes
        )
        print(f"Actualización exitosa: {response}")
    except botocore.exceptions.ClientError as e:
        print(f"Error al actualizar la función Lambda: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def main():
    parser = argparse.ArgumentParser(description='Actualizar una función Lambda de AWS con un ZIP.')

    parser.add_argument('--lambda_name', required=True, help='El nombre de la función Lambda.')
    parser.add_argument('--lambda_code_path', required=True, help='La ruta al código fuente de la función Lambda.')

    args = parser.parse_args()

    # Llamar a la función para actualizar la Lambda
    update_lambda(
        lambda_name=args.lambda_name,
        lambda_code_path=args.lambda_code_path
    )


if __name__ == '__main__':
    main()

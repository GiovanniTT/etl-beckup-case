## IMPORT
import os
from typing import List
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID') 
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION =os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

## Configura o cliente S3
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    print("Cliente S3 configurado com sucesso.")
except Exception as e:
    print(f"Erro ao configurar o cliente S3: {e}")
    raise

## LE OS ARQUIVOS
def listar_arquivos(directory):
    if not os.path.exists(directory):
        raise Exception(f"Pasta '{directory}' não existe.")

    files = []
    for file_name in os.listdir(directory): 
        local_file = os.path.join(directory, file_name) 
        if os.path.isfile(local_file): 
            files.append(local_file)
    return files

## JOGA OS ARQUIVOS PRO S3
def upload_arquivos_para_s3(arquivos):
    """Faz upload dos arquivos listados para o S3."""
    for arquivo in arquivos:
        nome_arquivo: str = os.path.basename(arquivo)
        try:
            print(f"Tentando fazer upload de '{nome_arquivo}' para o bucket '{BUCKET_NAME}'...")
            s3_client.upload_file(arquivo, BUCKET_NAME, nome_arquivo)
            print(f"{nome_arquivo} foi enviado para o S3.")
        except Exception as e:
            print(f"Erro ao enviar '{nome_arquivo}' para o S3: {e}")
            raise

## DELETA OS ARQUIVOS LOCAIS
def deletar_arquivos_locais(arquivos: List[str]) -> None:
    """Deleta os arquivos locais após o upload."""
    for arquivo in arquivos:
        try:
            os.remove(arquivo)
            print(f"{arquivo} foi deletado do local.")
        except Exception as e:
            print(f"Erro ao deletar o arquivo '{arquivo}': {e}")
            raise

## PIPILEINE

def executar_backup(pasta: str) -> None:
    try:
        print(f"Iniciando o processo de backup para a pasta '{pasta}'...")
        
        arquivos: List[str] = listar_arquivos(pasta)
        
        if arquivos:
            upload_arquivos_para_s3(arquivos)
            deletar_arquivos_locais(arquivos)
        else:
            print("Nenhum arquivo encontrado para backup.")
    except Exception as e:
        print(f"Erro no processo de backup: {e}")
        raise
    
if __name__ == "__main__":
    PASTA_LOCAL: str = 'download'  # Substitua pelo caminho da sua pasta local
    try:
        executar_backup(PASTA_LOCAL)
    except Exception as e:
        print(f"Erro ao executar o backup: {e}")
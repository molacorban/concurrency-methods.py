import io
import os
from os import getenv
from zipfile import ZipFile
from multiprocessing.pool import ThreadPool

import boto3
from dotenv import load_dotenv
from pandas import read_csv

from logger import logger


class Crawler():
    def __init__(self, s3):
        self.s3 = s3
        self.zip_obj = None

    def upload_arquivo_s3(self, arquivo: bytes) -> None:
        """Faz upload de um arquivo em modo binário para um Bucket
        Args:
            arquivo (bytes): arquivo para upload
        """
        path = getenv("FILE_PREFIX")
        caminho_arquivo_s3 = f"{path}/threadPool/{os.path.basename(arquivo)}"
        logger.info("Realizando upload para s3 ...")
        self.s3.upload_fileobj(
            Fileobj=self.zip_obj.open(arquivo),
            Bucket=getenv('S3_BUCKET_NAME'),
            Key=caminho_arquivo_s3)

    def store_zip_content(self, zip_content: bytes) -> list:
        """Salva todos os arquivos contidos em um zip para um Bucket utilizando pool de Threads
        Returns:
            list: lista de arquivos
        """
        self.zip_obj = ZipFile(io.BytesIO(zip_content), "r")
        lista_arquivos = self.zip_obj.namelist()
        pool = ThreadPool()
        pool.map(self.upload_arquivo_s3, lista_arquivos)
        return lista_arquivos

    def run(self):
        with open("resources/example.zip", "rb") as zipExamples:
            zipBytes = zipExamples.read()
            arquivos = self.store_zip_content(zipBytes)
        return arquivos


if __name__ == "__main__":
    df = read_csv("benchmark/result.csv")
    load_dotenv()
    s3 = boto3.client(
        's3',
        aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY')
    )
    crawler = Crawler(s3)
    arquivos = crawler.run()
    df = df.append(
        {"method": "thread", "time": 10, "arquivos_count": len(arquivos)},
        ignore_index=True)


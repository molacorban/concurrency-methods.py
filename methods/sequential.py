import io
import os
from os import getenv
from zipfile import ZipFile
import datetime

import boto3
from dotenv import load_dotenv
from pandas import read_csv

from logger import logger


class Crawler():
    def __init__(self, s3):
        self.s3 = s3
        self.zip_obj = None

    def upload_arquivo_s3(self, arquivo: bytes) -> None:
        path = getenv("FILE_PREFIX")
        caminho_arquivo_s3 = f"{path}/sequential/{os.path.basename(arquivo)}"
        logger.info("Realizando upload para s3 ...")
        self.s3.upload_fileobj(
            Fileobj=self.zip_obj.open(arquivo),
            Bucket=getenv('S3_BUCKET_NAME'),
            Key=caminho_arquivo_s3)

    def store_zip_content(self, zip_content: bytes) -> list:
        self.zip_obj = ZipFile(io.BytesIO(zip_content), "r")
        lista_arquivos = self.zip_obj.namelist()
        for arquivo in lista_arquivos:
            self.upload_arquivo_s3(arquivo)
        return lista_arquivos

    def run(self):
        with open(getenv("RESOURCE_FILE"), "rb") as zipExamples:
            zipBytes = zipExamples.read()
            arquivos = self.store_zip_content(zipBytes)
        return arquivos

def main():
    benchmark_path = getenv("BENCHMARK_FILE")
    df = read_csv(benchmark_path)
    s3 = boto3.client(
        's3',
        aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY')
    )
    time_init = datetime.datetime.now()
    crawler = Crawler(s3)
    arquivos = crawler.run()
    delta = datetime.datetime.now() - time_init
    data = {"method": "sequential", "time": delta.total_seconds(), "arquivos_count": len(arquivos)}
    logger.info(f"Finalizado: {data}")
    df = df.append(data, ignore_index=True)
    df.to_csv(benchmark_path, index=False)


if __name__ == "__main__":
    load_dotenv()
    main()

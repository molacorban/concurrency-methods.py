import os
import io
from os import getenv
import asyncio
from zipfile import ZipFile
import datetime

from aiobotocore.session import get_session
from dotenv import load_dotenv
from pandas import read_csv

from logger import logger


class Crawler:
    def __init__(self, s3):
        self.s3 = s3
        self.zip_obj = None

    async def upload_arquivo_s3(self, arquivo: bytes):
        path = getenv("FILE_PREFIX")
        caminho_arquivo_s3 = f"{path}/asyncio/{os.path.basename(arquivo)}"
        logger.info("Realizando upload para s3 ...")
        await self.s3.put_object(
            Body=self.zip_obj.open(arquivo, "r").read(),
            Bucket=getenv('S3_BUCKET_NAME'),
            Key=caminho_arquivo_s3)

    async def store_zip_content(self, zip_content: bytes) -> list:
        self.zip_obj = ZipFile(io.BytesIO(zip_content), "r")
        lista_arquivos = self.zip_obj.namelist()
        tasks = []
        for arquivo in lista_arquivos:
            task = self.upload_arquivo_s3(arquivo)
            tasks.append(task)
        await asyncio.gather(*tasks)
        return lista_arquivos

    async def run(self):
        with open(getenv("RESOURCE_FILE"), "rb") as zipExamples:
            zipBytes = zipExamples.read()
            arquivos = await self.store_zip_content(zipBytes)
        return arquivos

async def main():
    benchmark_path = getenv("BENCHMARK_FILE")
    df = read_csv(benchmark_path)
    session = get_session()
    async with session.create_client('s3',
            aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY')) as s3:
        crawler = Crawler(s3)
        time_init = datetime.datetime.now()
        arquivos = await crawler.run()
        delta = datetime.datetime.now() - time_init
    data = {"method": "asyncio", "time": delta.total_seconds(), "arquivos_count": len(arquivos)}
    logger.info(f"Finalizado: {data}")
    df = df.append(data, ignore_index=True)
    df.to_csv(benchmark_path, index=False)


if __name__ == "__main__":
    load_dotenv()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

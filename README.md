# Formas de concorrência em python

Foi feito uma comparação entre concorrência utilizando thread's reais, e utilizando corrotinas, atráves da biblioteca [asyncio](https://docs.python.org/3/library/asyncio.html).

Para fazer a comparação dois dois métodos, foi utilizando a situação onde é feito decompactado um arquivo de zip, com uma determinada quantidade de arquivos, e feito upload de todos os arquivos para um banco de dados semi-estruturado, que no caso, foi o serviço s3 da aws. Ou seja, trata-se de um experimento onde maior parte do tempo é gasto em tarefas de IO, que é um caso também chamado de IO-Bound.

![Resultados em gráficos](benchmark/result.png)

# Formas de concorrência em python

Foi feito uma comparação entre concorrência utilizando thread's reais, e utilizando corrotinas, atráves da biblioteca [asyncio](https://docs.python.org/3/library/asyncio.html).

Para fazer a comparação dos dois métodos, foi utilizando a situação onde é decompactado um arquivo zip, com uma determinada quantidade de arquivos, e feito upload de todos os arquivos para um banco de dados semi-estruturado, que no caso, foi o serviço s3 da aws. Ou seja, trata-se de um experimento onde maior parte do tempo é gasto em tarefas de IO, que é um caso também chamado de IO-Bound.

Para criar corrotinas utilizando a sintaxe `async/await` é importante que as bibliotecas utilizadas suportem asyncronia, com isso, para fazer upload na versão que utiliza asyncronia foi utilizado a biblioteca [aiobotocore](https://github.com/aio-libs/aiobotocore) que é a versão asyncrona do botocore. 

## Resultados

![Resultados em gráficos](benchmark/result.png)

## Como reproduzir

É necessário criar um ambiente vitual utilizando a biblioteca `venv`, após isso é necessário instalar todas as bibliotecas descritas no requirements. Ademais, deve-se criar um arquivo `.env` com as variáveis de ambiente descritas em `.env.example`. Com isso, o ambiente está pronto.

Com o ambiente pronto, é necessário criar o arquivo zip para fazer upload. É utilizado esse comandos:

```
make create-zip FILES_IN_ZIP=500
```

Nesse caso é criado um arquivo zip com 500 arquivos de 100KB cada. 

Agora para executar o experimento pode se utilizar o comando:

```
make asyncio-exec && make thread-exec && make sequential-exec
```

Com isso, é executado o experimento nas três diferentes formas. O resultado com tempo de cada uma é salvo em um arquivo `.csv`.

Após fazer o experimento algumas vezes, com diferentes quantidades de arquivos, para ver o resultado de forma gráfica, utilize o comando:

```
make show-plot
```

## Contribuições

Qualquer forma de contribuição é bem-vinda, basta abrir um issue ou PR. Obrigado :rocket:



from os import getenv

from pandas import read_csv
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from logger import logger


def get_methods(df):
    methods = set()
    for method in df["method"]:
        methods.add(method)
    return methods

def plot(df, method):
    plt.plot(df["arquivos_count"], df["time"], label=method)

def prepare_to_save():
    plt.legend()
    plt.xlabel("upload file (100k)")
    plt.ylabel("Seconds (s)")
    plt.title("Processo de Upload para s3")

def save_fig():
    logger.info("Saving figure...")
    plt.savefig(getenv("PLOT_FILE"))


def main():
    df = read_csv(getenv("BENCHMARK_FILE"))
    methods = get_methods(df)
    for method in methods:
        df_filtered = df[df["method"] == method]
        plot(df_filtered, method)
    prepare_to_save()
    save_fig()


if __name__ == "__main__":
    load_dotenv()
    main()


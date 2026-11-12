UNIDADES = ["B", "KB", "MB", "GB", "TB"]


def formatar_bytes(tamanho: int) -> str:
    """Formata um tamanho em bytes para leitura humana (base 1024)."""
    if tamanho < 0:
        raise ValueError("tamanho não pode ser negativo")
    valor = float(tamanho)
    for unidade in UNIDADES:
        if valor < 1024 or unidade == UNIDADES[-1]:
            return f"{valor:.1f} {unidade}"
        valor /= 1024

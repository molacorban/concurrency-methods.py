import pytest

from utils.tamanho import formatar_bytes


def test_bytes():
    assert formatar_bytes(500) == "500.0 B"


def test_kilobytes():
    assert formatar_bytes(2048) == "2.0 KB"


def test_maior_unidade():
    assert formatar_bytes(1024 ** 5) == "1024.0 TB"


def test_negativo():
    with pytest.raises(ValueError):
        formatar_bytes(-1)

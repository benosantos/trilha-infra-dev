
import pytest

from src.normalizacao import (
    normalizar_linha,
    normalizar_serie
)


# ==========================================
# TESTES DE TELEFONE VÁLIDO
# ==========================================

@pytest.mark.parametrize("entrada, esperado", [
    ("(11) 91234-5678", "11912345678"),
    ("+55 11 91234 5678", "11912345678"),
    ("5511912345678", "11912345678"),
    ("(21) 3234-5678", "2132345678"),
    ("11987654321", "11987654321"),
    ("551132345678", "1132345678"),
    ("(31) 99876-5432", "31998765432"),
])
def test_normalizar_linha_ok(entrada, esperado):

    resultado = normalizar_linha(entrada)

    assert resultado["valor"] == esperado
    assert resultado["status"] == "OK"
    assert "motivo" not in resultado


# ==========================================
# TESTES DE TELEFONE INVÁLIDO
# ==========================================

@pytest.mark.parametrize("entrada", [
    "",
    "abc",
    "123",
    "00000000000",
    "11912abc5678",
    None,
    "123456789012345",
])
def test_normalizar_linha_revisar(entrada):

    resultado = normalizar_linha(entrada)

    assert resultado["valor"] is None
    assert resultado["status"] == "REVISAR"
    assert "motivo" in resultado


# ==========================================
# TESTE DE TELEFONE SEM DDD
# ==========================================

def test_telefone_sem_ddd():

    resultado = normalizar_linha("91234-5678")

    assert resultado["valor"] is None
    assert resultado["status"] == "REVISAR"
    assert resultado["motivo"] == "sem DDD"


# ==========================================
# TESTE DE TELEFONE COM LETRAS
# ==========================================

def test_telefone_com_letras():

    resultado = normalizar_linha("11912abc5678")

    assert resultado["valor"] is None
    assert resultado["status"] == "REVISAR"
    assert resultado["motivo"] == "telefone contém caracteres inválidos"


# ==========================================
# TESTE DE DDD INVÁLIDO
# ==========================================

def test_telefone_com_ddd_invalido():

    resultado = normalizar_linha("00123456789")

    assert resultado["valor"] is None
    assert resultado["status"] == "REVISAR"
    assert resultado["motivo"] == "DDD inválido"

# ==========================================
# TESTES DE SÉRIE VÁLIDA
# ==========================================

@pytest.mark.parametrize("entrada, esperado", [
    ("pf3a  9x7k", "PF3A9X7K"),
    ("5xk2j93", "5XK2J93"),
    ("ABC 123", "ABC123"),
    ("  Dell 123  ", "DELL123"),
])
def test_normalizar_serie_ok(entrada, esperado):

    resultado = normalizar_serie(entrada)

    assert resultado["valor"] == esperado
    assert resultado["status"] == "OK"
    assert "motivo" not in resultado


# ==========================================
# TESTES DE SÉRIE DESCONHECIDA
# ==========================================

@pytest.mark.parametrize("entrada", [
    "Não sei",
    "nao sei",
    "-",
    "",
    "   ",
    None,
])
def test_normalizar_serie_revisar(entrada):

    resultado = normalizar_serie(entrada)

    assert resultado["valor"] is None
    assert resultado["status"] == "REVISAR"
    assert "motivo" in resultado


# ==========================================
# TESTE DE SÉRIE COM ACENTUAÇÃO
# ==========================================

def test_serie_desconhecida_com_acento():

    resultado = normalizar_serie("NÃO SEI")

    assert resultado["valor"] is None
    assert resultado["status"] == "REVISAR"
    assert resultado["motivo"] == "série desconhecida"


# ==========================================
# TESTE DE SÉRIE COM ESPAÇOS
# ==========================================

def test_serie_remove_todos_os_espacos():

    resultado = normalizar_serie("  PF 3A 9X 7K  ")

    assert resultado["valor"] == "PF3A9X7K"
    assert resultado["status"] == "OK"

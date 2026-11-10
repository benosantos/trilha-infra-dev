
import json
import multiprocessing
from pathlib import Path

import pytest

from dev02_patrimonio.src.patrimonio import (
    gerar_patrimonio,
    inicializar_arquivo,
    carregar_dados
)

@pytest.fixture
def arquivo_teste(tmp_path):
    """
    Cria um arquivo JSON isolado para cada teste.
    """

    caminho = tmp_path / "patrimonio.json"

    inicializar_arquivo(caminho)

    return caminho


# ==========================================
# TESTE DE GERAÇÃO DE PATRIMÔNIO
# ==========================================

def test_gerar_primeiro_notebook(arquivo_teste):

    resultado = gerar_patrimonio("NB", arquivo_teste)

    assert resultado == "PAT-NB-0001"


def test_gerar_segundo_notebook(arquivo_teste):

    gerar_patrimonio("NB", arquivo_teste)

    resultado = gerar_patrimonio("NB", arquivo_teste)

    assert resultado == "PAT-NB-0002"


# ==========================================
# TESTE DE CONTADORES INDEPENDENTES
# ==========================================

def test_contadores_separados_por_tipo(arquivo_teste):

    notebook = gerar_patrimonio("NB", arquivo_teste)
    desktop = gerar_patrimonio("DT", arquivo_teste)
    monitor = gerar_patrimonio("MN", arquivo_teste)

    assert notebook == "PAT-NB-0001"
    assert desktop == "PAT-DT-0001"
    assert monitor == "PAT-MN-0001"


# ==========================================
# TESTE DE TIPO DESCONHECIDO
# ==========================================

@pytest.mark.parametrize("tipo", [
    "TV",
    "IMPRESSORA",
    "SERVIDOR",
    "",
    "123",
])
def test_tipo_desconhecido(arquivo_teste, tipo):

    with pytest.raises(ValueError):
        gerar_patrimonio(tipo, arquivo_teste)


def test_tipo_minusculo(arquivo_teste):

    resultado = gerar_patrimonio("nb", arquivo_teste)

    assert resultado == "PAT-NB-0001"


# ==========================================
# TESTE DE PERSISTÊNCIA
# ==========================================

def test_persistencia_apos_reiniciar(arquivo_teste):

    primeiro = gerar_patrimonio("NB", arquivo_teste)

    # Simula uma nova execução da função.
    segundo = gerar_patrimonio("NB", arquivo_teste)

    assert primeiro == "PAT-NB-0001"
    assert segundo == "PAT-NB-0002"


# ==========================================
# TESTE DE FORMATO COM MAIS DE 9999
# ==========================================

def test_numero_maior_que_9999(arquivo_teste):

    dados = carregar_dados(arquivo_teste)

    dados["NB"] = 9999

    arquivo_teste.write_text(
        json.dumps(dados),
        encoding="utf-8"
    )

    resultado = gerar_patrimonio("NB", arquivo_teste)

    assert resultado == "PAT-NB-10000"


# ==========================================
# TESTE DE ARQUIVO INEXISTENTE
# ==========================================

def test_criar_arquivo_automaticamente(tmp_path):

    caminho = tmp_path / "novo" / "patrimonio.json"

    resultado = gerar_patrimonio("NB", caminho)

    assert resultado == "PAT-NB-0001"
    assert caminho.exists()


# ==========================================
# TESTE DE JSON CORROMPIDO
# ==========================================

def test_json_corrompido(arquivo_teste):

    arquivo_teste.write_text(
        "{ JSON INVALIDO",
        encoding="utf-8"
    )

    with pytest.raises(RuntimeError):
        gerar_patrimonio("NB", arquivo_teste)


# ==========================================
# TESTE DE CONCORRÊNCIA
# ==========================================

def trabalhador(caminho, quantidade, fila):

    codigos = []

    for _ in range(quantidade):
        codigo = gerar_patrimonio("NB", caminho)
        codigos.append(codigo)

    fila.put(codigos)


def test_concorrencia_1000_patrimonios(arquivo_teste):

    quantidade_processos = 20
    codigos_por_processo = 50

    fila = multiprocessing.Queue()

    processos = []

    for _ in range(quantidade_processos):

        processo = multiprocessing.Process(
            target=trabalhador,
            args=(
                str(arquivo_teste),
                codigos_por_processo,
                fila
            )
        )

        processos.append(processo)
        processo.start()

    for processo in processos:
        processo.join(timeout=60)

    # Verifica se todos os processos terminaram.
    for processo in processos:
        assert processo.exitcode == 0

    todos_codigos = []

    for _ in range(quantidade_processos):
        todos_codigos.extend(
            fila.get(timeout=10)
        )

    # Verifica a quantidade total.
    assert len(todos_codigos) == 1000

    # Verifica se não existem duplicidades.
    assert len(set(todos_codigos)) == 1000

    # Verifica a sequência completa.
    esperados = {
        f"PAT-NB-{numero:04d}"
        for numero in range(1, 1001)
    }

    assert set(todos_codigos) == esperados

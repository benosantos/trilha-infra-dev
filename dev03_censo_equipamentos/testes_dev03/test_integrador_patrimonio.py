
import json

from dev03_censo_equipamentos.src.integrador_patrimonio import (
    atribuir_patrimonios,
    ARQUIVO_PATRIMONIO,
)


def test_gerar_patrimonio_para_itens(tmp_path, monkeypatch):
    caminho = tmp_path / "patrimonio.json"

    monkeypatch.setattr(
        "dev03_censo_equipamentos.src.integrador_patrimonio.ARQUIVO_PATRIMONIO",
        caminho,
    )

    itens = [
        {"tipo": "NB", "patrimonio": None},
        {"tipo": "CL", "patrimonio": None},
        {"tipo": "CH", "patrimonio": None},
    ]

    resultado = atribuir_patrimonios(itens)

    assert resultado[0]["patrimonio"] == "PAT-NB-0001"
    assert resultado[1]["patrimonio"] == "PAT-CL-0001"
    assert resultado[2]["patrimonio"] == "PAT-CH-0001"


def test_contadores_independentes(tmp_path, monkeypatch):
    caminho = tmp_path / "patrimonio.json"

    monkeypatch.setattr(
        "dev03_censo_equipamentos.src.integrador_patrimonio.ARQUIVO_PATRIMONIO",
        caminho,
    )

    itens = [
        {"tipo": "NB", "patrimonio": None},
        {"tipo": "NB", "patrimonio": None},
    ]

    resultado = atribuir_patrimonios(itens)

    assert resultado[0]["patrimonio"] == "PAT-NB-0001"
    assert resultado[1]["patrimonio"] == "PAT-NB-0002"


def test_nao_gerar_patrimonio_duplicado(tmp_path, monkeypatch):
    caminho = tmp_path / "patrimonio.json"

    monkeypatch.setattr(
        "dev03_censo_equipamentos.src.integrador_patrimonio.ARQUIVO_PATRIMONIO",
        caminho,
    )

    itens = [
        {"tipo": "NB", "patrimonio": "PAT-NB-0099"},
    ]

    resultado = atribuir_patrimonios(itens)

    assert resultado[0]["patrimonio"] == "PAT-NB-0099"

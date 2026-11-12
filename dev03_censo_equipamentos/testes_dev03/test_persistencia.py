
import json
import pytest

from dev03_censo_equipamentos.src.persistencia import (
    carregar_itens,
    salvar_itens,
    mesclar_itens,
)


def item(patrimonio="PAT-NB-0001"):
    return {
        "identificador": "20261112083000#Analista de TI",
        "tipo": "NB",
        "equipamento": "Notebook",
        "patrimonio": patrimonio,
    }


def test_carregar_arquivo_inexistente(tmp_path):
    caminho = tmp_path / "itens.json"

    assert carregar_itens(caminho) == []


def test_salvar_e_carregar_itens(tmp_path):
    caminho = tmp_path / "itens.json"

    itens = [item()]

    salvar_itens(itens, caminho)

    resultado = carregar_itens(caminho)

    assert resultado == itens


def test_mesclar_novo_item():
    existentes = []
    novos = [item()]

    resultado = mesclar_itens(existentes, novos)

    assert len(resultado) == 1


def test_nao_duplicar_item():
    existentes = [item()]
    novos = [item()]

    resultado = mesclar_itens(existentes, novos)

    assert len(resultado) == 1


def test_adicionar_item_diferente():
    existentes = [item()]

    novo = item()
    novo["tipo"] = "CL"
    novo["patrimonio"] = "PAT-CL-0001"

    resultado = mesclar_itens(existentes, [novo])

    assert len(resultado) == 2


def test_json_corrompido(tmp_path):
    caminho = tmp_path / "itens.json"

    caminho.write_text(
        "{json inválido",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="JSON inválido"):
        carregar_itens(caminho)


def test_json_com_estrutura_invalida(tmp_path):
    caminho = tmp_path / "itens.json"

    caminho.write_text(
        json.dumps({"itens": []}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="deve conter uma lista"):
        carregar_itens(caminho)


def test_rejeitar_item_sem_patrimonio(tmp_path):
    caminho = tmp_path / "itens.json"

    salvar_itens(
        [{"identificador": "123#TI", "tipo": "NB"}],
        caminho,
    )

    with pytest.raises(ValueError, match="sem patrimônio"):
        carregar_itens(caminho)


def test_rejeitar_itens_duplicados(tmp_path):
    caminho = tmp_path / "itens.json"

    salvar_itens([item(), item()], caminho)

    with pytest.raises(ValueError, match="duplicados"):
        carregar_itens(caminho)

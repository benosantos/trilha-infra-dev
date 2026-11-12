
import pytest

from dev03_censo_equipamentos.src.gerador_itens import (
    criar_identificador,
    gerar_itens_funcionario,
)


def funcionario():
    return {
        "carimbo": "2026-11-12 08:30:00",
        "nome": "Joao Silva",
        "telefone": "(11) 91234-5678",
        "vaga": "Analista de TI",
        "notebook": "Sim",
        "serie_notebook": "PF3A 9X7K",
        "celular": "Sim",
        "serie_celular": "ABC123",
        "chip": "Sim",
        "linha_chip": "(11) 99876-5432",
    }


def test_gerar_tres_equipamentos():
    itens = gerar_itens_funcionario(funcionario())

    assert len(itens) == 3

    assert [item["tipo"] for item in itens] == [
        "NB", "CL", "CH"
    ]


def test_gerar_apenas_equipamentos_com_sim():
    dados = funcionario()

    dados["notebook"] = "Não"
    dados["chip"] = "Não"

    itens = gerar_itens_funcionario(dados)

    assert len(itens) == 1
    assert itens[0]["tipo"] == "CL"


def test_normalizar_serie_notebook():
    itens = gerar_itens_funcionario(funcionario())

    notebook = itens[0]

    assert notebook["serie"] == "PF3A9X7K"
    assert notebook["status_serie"] == "OK"


def test_serie_desconhecida_gera_revisao():
    dados = funcionario()
    dados["serie_celular"] = "Nao sei"

    itens = gerar_itens_funcionario(dados)

    celular = itens[1]

    assert celular["serie"] is None
    assert celular["status_serie"] == "REVISAR"
    assert "motivo_serie" in celular


def test_normalizar_telefone():
    itens = gerar_itens_funcionario(funcionario())

    assert itens[0]["telefone"] == "11912345678"
    assert itens[0]["status_telefone"] == "OK"


def test_identificador():
    identificador = criar_identificador(
        "2026-11-12 08:30:00",
        "Analista de TI",
    )

    assert identificador == (
        "20261112083000#Analista de TI"
    )


def test_carimbo_invalido():
    dados = funcionario()
    dados["carimbo"] = "data inválida"

    with pytest.raises(ValueError, match="Carimbo inválido"):
        gerar_itens_funcionario(dados)


def test_vaga_obrigatoria():
    dados = funcionario()
    dados["vaga"] = ""

    with pytest.raises(ValueError, match="Carimbo e vaga"):
        gerar_itens_funcionario(dados)

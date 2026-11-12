
import csv

import pytest

from dev03_censo_equipamentos.src.leitor_csv import ler_respostas


COLUNAS = [
    "carimbo",
    "nome",
    "telefone",
    "vaga",
    "notebook",
    "serie_notebook",
    "celular",
    "serie_celular",
    "chip",
    "linha_chip",
]


def criar_csv(caminho, linhas):
    with caminho.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=COLUNAS
        )
        escritor.writeheader()
        escritor.writerows(linhas)


def funcionario(nome="Joao Silva"):
    return {
        "carimbo": "2026-11-12 08:30:00",
        "nome": nome,
        "telefone": "11912345678",
        "vaga": "Analista de TI",
        "notebook": "Sim",
        "serie_notebook": "PF3A 9X7K",
        "celular": "Não",
        "serie_celular": "",
        "chip": "Sim",
        "linha_chip": "11987654321",
    }


def test_ler_csv_com_funcionario_valido(tmp_path):
    caminho = tmp_path / "respostas.csv"

    criar_csv(caminho, [funcionario()])

    resultado = ler_respostas(caminho)

    assert len(resultado) == 1
    assert resultado[0]["nome"] == "Joao Silva"


def test_ignorar_funcionario_teste(tmp_path):
    caminho = tmp_path / "respostas.csv"

    criar_csv(
        caminho,
        [
            funcionario("Joao Silva"),
            funcionario("TESTE Automático"),
        ],
    )

    resultado = ler_respostas(caminho)

    assert len(resultado) == 1
    assert resultado[0]["nome"] == "Joao Silva"


def test_ignorar_nome_vazio(tmp_path):
    caminho = tmp_path / "respostas.csv"

    criar_csv(
        caminho,
        [funcionario("   ")],
    )

    resultado = ler_respostas(caminho)

    assert resultado == []


def test_arquivo_inexistente():
    with pytest.raises(FileNotFoundError):
        ler_respostas("arquivo_inexistente.csv")


def test_csv_sem_cabecalho(tmp_path):
    caminho = tmp_path / "respostas.csv"
    caminho.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="cabeçalho"):
        ler_respostas(caminho)


def test_colunas_obrigatorias_ausentes(tmp_path):
    caminho = tmp_path / "respostas.csv"

    caminho.write_text(
        "nome,telefone\nJoao,11912345678\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Colunas obrigatórias"):
        ler_respostas(caminho)


import csv
from pathlib import Path


COLUNAS_OBRIGATORIAS = {
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
}


def ler_respostas(caminho):
    """
    Lê as respostas de um arquivo CSV.

    Ignora funcionários cujo nome começa com TESTE.

    Retorna uma lista de dicionários.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {caminho}"
        )

    with caminho.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        if not leitor.fieldnames:
            raise ValueError("O CSV não possui cabeçalho.")

        colunas = {
            coluna.strip()
            for coluna in leitor.fieldnames
            if coluna
        }

        faltantes = COLUNAS_OBRIGATORIAS - colunas

        if faltantes:
            raise ValueError(
                f"Colunas obrigatórias ausentes: {sorted(faltantes)}"
            )

        funcionarios = []

        for linha in leitor:
            nome = (linha.get("nome") or "").strip()

            if not nome:
                continue

            if nome.upper().startswith("TESTE"):
                continue

            funcionarios.append({
                chave.strip(): (valor or "").strip()
                for chave, valor in linha.items()
                if chave is not None
            })

    return funcionarios

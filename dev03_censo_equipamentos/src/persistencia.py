
import json
import os
import tempfile

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_ITENS = BASE_DIR / "data" / "itens.json"


def carregar_itens(caminho=ARQUIVO_ITENS):
    """Carrega os itens existentes."""

    caminho = Path(caminho)

    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    except json.JSONDecodeError as erro:
        raise ValueError(
            "Arquivo itens.json possui JSON inválido."
        ) from erro

    if not isinstance(dados, list):
        raise ValueError(
            "O arquivo itens.json deve conter uma lista."
        )

    identificadores = set()

    for item in dados:
        if not isinstance(item, dict):
            raise ValueError("Item inválido no arquivo.")

        chave = (
            item.get("identificador"),
            item.get("tipo"),
        )

        if not all(chave):
            raise ValueError("Item sem identificador ou tipo.")

        if not item.get("patrimonio"):
            raise ValueError("Item sem patrimônio.")

        if chave in identificadores:
            raise ValueError("Existem itens duplicados.")

        identificadores.add(chave)

    return dados


def salvar_itens(itens, caminho=ARQUIVO_ITENS):
    """Salva os itens usando substituição atômica."""

    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    arquivo_temporario = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=caminho.parent,
            suffix=".tmp",
            delete=False,
        ) as arquivo:

            arquivo_temporario = Path(arquivo.name)

            json.dump(
                itens,
                arquivo,
                indent=4,
                ensure_ascii=False,
            )

            arquivo.flush()
            os.fsync(arquivo.fileno())

        os.replace(arquivo_temporario, caminho)

    finally:
        if (
            arquivo_temporario
            and arquivo_temporario.exists()
        ):
            arquivo_temporario.unlink()


def mesclar_itens(existentes, novos):
    """
    Adiciona somente itens ainda não cadastrados.

    A chave de idempotência é:
    identificador + tipo.
    """

    resultado = list(existentes)

    chaves_existentes = {
        (item["identificador"], item["tipo"])
        for item in existentes
    }

    for item in novos:

        chave = (
            item["identificador"],
            item["tipo"],
        )

        if chave in chaves_existentes:
            continue

        resultado.append(item)
        chaves_existentes.add(chave)

    return resultado

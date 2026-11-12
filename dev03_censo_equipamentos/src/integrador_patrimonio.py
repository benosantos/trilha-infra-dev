
from pathlib import Path

from dev02_patrimonio.src.patrimonio import gerar_patrimonio


BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_PATRIMONIO = BASE_DIR / "data" / "patrimonio_dev03.json"


def atribuir_patrimonios(itens):
    """
    Atribui patrimônios aos itens do DEV-03.

    Utiliza a função original do DEV-02,
    mas mantém os contadores separados.
    """

    for item in itens:

        if item.get("patrimonio"):
            continue

        tipo = item["tipo"]

        item["patrimonio"] = gerar_patrimonio(
            tipo,
            caminho=ARQUIVO_PATRIMONIO,
        )

    return itens

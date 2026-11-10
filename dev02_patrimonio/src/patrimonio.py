
import json
from pathlib import Path

import portalocker


# Tipos de equipamentos permitidos
TIPOS_EQUIPAMENTOS = {
    "NB": "Notebook",
    "DT": "Desktop",
    "MN": "Monitor",
    "CL": "Celular",
    "CH": "Chip",
    "OU": "Outros",
}


# Caminho padrão do arquivo JSON
BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_DADOS = BASE_DIR / "data" / "patrimonio.json"

# Arquivo utilizado para controlar o acesso concorrente
ARQUIVO_LOCK = ARQUIVO_DADOS.with_suffix(".lock")


def inicializar_arquivo(caminho=ARQUIVO_DADOS):
    """
    Cria o arquivo JSON caso ainda não exista.
    """

    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    if not caminho.exists():
        dados_iniciais = {
            tipo: 0 for tipo in TIPOS_EQUIPAMENTOS
        }

        caminho.write_text(
            json.dumps(dados_iniciais, indent=4),
            encoding="utf-8"
        )


def carregar_dados(caminho=ARQUIVO_DADOS):
    """
    Carrega os últimos números de patrimônio.
    """

    caminho = Path(caminho)

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    except (OSError, json.JSONDecodeError) as erro:
        raise RuntimeError(
            f"Não foi possível ler o arquivo de patrimônio: {erro}"
        ) from erro

    if not isinstance(dados, dict):
        raise ValueError("O arquivo de patrimônio deve conter um objeto JSON.")

    for tipo in TIPOS_EQUIPAMENTOS:
        numero = dados.get(tipo)

        if (
            isinstance(numero, bool)
            or not isinstance(numero, int)
            or numero < 0
        ):
            raise ValueError(
                f"Contador inválido para o tipo {tipo}."
            )

    return dados


def gerar_patrimonio(tipo, caminho=ARQUIVO_DADOS):
    """
    Gera um patrimônio único e sequencial.

    O bloqueio de arquivo impede que processos simultâneos
    utilizem o mesmo número.
    """

    tipo = tipo.strip().upper() if isinstance(tipo, str) else ""

    if tipo not in TIPOS_EQUIPAMENTOS:
        raise ValueError(
            f"Tipo de equipamento inválido: {tipo}"
        )

    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    arquivo_lock = caminho.with_suffix(".lock")

    with portalocker.Lock(
        str(arquivo_lock),
        mode="a",
        timeout=30,
        encoding="utf-8"
    ):
        if not caminho.exists():
            inicializar_arquivo(caminho)

        dados = carregar_dados(caminho)

        # Incrementa o contador do tipo solicitado.
        proximo_numero = dados[tipo] + 1

        dados[tipo] = proximo_numero

        # Grava os dados atualizados.
        with caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )
            arquivo.flush()

        # Formata o patrimônio.
        codigo = f"PAT-{tipo}-{proximo_numero:04d}"

        return codigo

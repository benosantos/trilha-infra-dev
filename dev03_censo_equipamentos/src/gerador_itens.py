
from datetime import datetime

from dev01_normalizacao.src.normalizacao import (
    normalizar_linha,
    normalizar_serie,
)


def resposta_sim(valor):
    """Verifica se a resposta representa Sim."""
    return isinstance(valor, str) and valor.strip().casefold() == "sim"


def criar_identificador(carimbo, vaga):
    """Cria um identificador estável para a resposta."""
    carimbo = (carimbo or "").strip()
    vaga = (vaga or "").strip()

    if not carimbo or not vaga:
        raise ValueError("Carimbo e vaga são obrigatórios.")

    try:
        data = datetime.strptime(
            carimbo,
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError as erro:
        raise ValueError("Carimbo inválido.") from erro

    return f"{data:%Y%m%d%H%M%S}#{vaga}"


def gerar_itens_funcionario(funcionario):
    """
    Transforma um funcionário em itens individuais.

    Tipos:
    NB = Notebook
    CL = Celular
    CH = Chip
    """

    identificador = criar_identificador(
        funcionario.get("carimbo"),
        funcionario.get("vaga"),
    )

    telefone = normalizar_linha(
        funcionario.get("telefone")
    )

    itens = []

    equipamentos = [
        {
            "campo": "notebook",
            "tipo": "NB",
            "serie": "serie_notebook",
            "nome": "Notebook",
        },
        {
            "campo": "celular",
            "tipo": "CL",
            "serie": "serie_celular",
            "nome": "Celular",
        },
        {
            "campo": "chip",
            "tipo": "CH",
            "serie": None,
            "nome": "Chip",
        },
    ]

    for equipamento in equipamentos:

        if not resposta_sim(
            funcionario.get(equipamento["campo"])
        ):
            continue

        item = {
            "identificador": identificador,
            "funcionario": funcionario.get("nome"),
            "vaga": funcionario.get("vaga"),
            "tipo": equipamento["tipo"],
            "equipamento": equipamento["nome"],
            "telefone": telefone["valor"],
            "status_telefone": telefone["status"],
            "serie": None,
            "status_serie": "NAO_APLICAVEL",
            "patrimonio": None,
        }

        if equipamento["serie"]:
            serie = normalizar_serie(
                funcionario.get(equipamento["serie"])
            )

            item["serie"] = serie["valor"]
            item["status_serie"] = serie["status"]

            if serie["status"] == "REVISAR":
                item["motivo_serie"] = serie["motivo"]

        if telefone["status"] == "REVISAR":
            item["motivo_telefone"] = telefone["motivo"]

        itens.append(item)

    return itens

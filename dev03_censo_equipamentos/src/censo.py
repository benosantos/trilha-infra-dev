
import portalocker

from pathlib import Path

from dev03_censo_equipamentos.src.leitor_csv import ler_respostas

from dev03_censo_equipamentos.src.gerador_itens import (
    gerar_itens_funcionario,
)

from dev03_censo_equipamentos.src.integrador_patrimonio import (
    atribuir_patrimonios,
)

from dev03_censo_equipamentos.src.persistencia import (
    carregar_itens,
    salvar_itens,
    mesclar_itens,
)


# ==================================================
# CONFIGURAÇÕES
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ARQUIVO_CSV = BASE_DIR / "data" / "respostas.csv"

ARQUIVO_ITENS = BASE_DIR / "data" / "itens.json"

ARQUIVO_LOCK = ARQUIVO_ITENS.with_suffix(".lock")


# ==================================================
# PROCESSAMENTO DO CENSO
# ==================================================

def processar_censo(
    caminho_csv=ARQUIVO_CSV,
    caminho_itens=ARQUIVO_ITENS,
):
    """
    Processa o censo completo de equipamentos.

    Funcionalidades:
    - Leitura do CSV.
    - Geração de equipamentos individuais.
    - Integração com DEV-01.
    - Integração com DEV-02.
    - Controle de duplicidade.
    - Geração de patrimônios.
    - Persistência em JSON.
    - Bloqueio de concorrência.
    - Identificação de pendências.
    """

    caminho_csv = Path(caminho_csv)
    caminho_itens = Path(caminho_itens)

    caminho_itens.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_lock = caminho_itens.with_suffix(".lock")

    # Impede duas execuções simultâneas
    with portalocker.Lock(
        str(caminho_lock),
        mode="a",
        timeout=30,
        encoding="utf-8",
    ):

        # 1. Ler funcionários
        funcionarios = ler_respostas(caminho_csv)

        # 2. Carregar itens cadastrados
        itens_existentes = carregar_itens(caminho_itens)

        # 3. Identificar itens já existentes
        chaves_existentes = {
            (
                item["identificador"],
                item["tipo"],
            )
            for item in itens_existentes
        }

        itens_novos = []

        # 4. Gerar equipamentos individuais
        for funcionario in funcionarios:

            itens_funcionario = gerar_itens_funcionario(
                funcionario
            )

            for item in itens_funcionario:

                chave = (
                    item["identificador"],
                    item["tipo"],
                )

                if chave not in chaves_existentes:

                    itens_novos.append(item)

                    chaves_existentes.add(chave)

        # 5. Gerar patrimônios para os novos itens
        if itens_novos:

            atribuir_patrimonios(itens_novos)

        # 6. Mesclar registros
        resultado = mesclar_itens(
            itens_existentes,
            itens_novos,
        )

        # 7. Salvar resultados
        salvar_itens(
            resultado,
            caminho_itens,
        )

        # 8. Identificar pendências
        pendencias = [
            item
            for item in resultado
            if (
                item.get("status_telefone") == "REVISAR"
                or item.get("status_serie") == "REVISAR"
            )
        ]

        # 9. Retornar resumo
        return {
            "funcionarios_lidos": len(funcionarios),
            "itens_existentes": len(itens_existentes),
            "itens_novos": len(itens_novos),
            "total_itens": len(resultado),
            "pendencias": len(pendencias),
            "itens": resultado,
        }


# ==================================================
# RELATÓRIO DO CENSO
# ==================================================

def exibir_resumo(resultado):
    """
    Exibe o resumo do processamento
    e as pendências de revisão.
    """

    print("\n" + "=" * 50)
    print("          CENSO DE EQUIPAMENTOS")
    print("=" * 50)

    print(
        f"Funcionários lidos: "
        f"{resultado['funcionarios_lidos']}"
    )

    print(
        f"Itens já cadastrados: "
        f"{resultado['itens_existentes']}"
    )

    print(
        f"Itens novos: "
        f"{resultado['itens_novos']}"
    )

    print(
        f"Total de itens: "
        f"{resultado['total_itens']}"
    )

    print(
        f"Pendências de revisão: "
        f"{resultado['pendencias']}"
    )

    print("=" * 50)

    if resultado["pendencias"]:

        print("\nITENS QUE PRECISAM DE REVISÃO")

        for item in resultado["itens"]:

            motivos = []

            if item.get("status_telefone") == "REVISAR":

                motivos.append(
                    item.get(
                        "motivo_telefone",
                        "Telefone inválido",
                    )
                )

            if item.get("status_serie") == "REVISAR":

                motivos.append(
                    item.get(
                        "motivo_serie",
                        "Série inválida",
                    )
                )

            if motivos:

                print(
                    f"- {item['identificador']} | "
                    f"{item['tipo']} | "
                    f"{', '.join(motivos)}"
                )

    else:

        print("\nNenhuma pendência encontrada.")

    print("\nProcessamento concluído!")
    print("=" * 50)


# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================

if __name__ == "__main__":

    try:

        resultado = processar_censo()

        exibir_resumo(resultado)

    except Exception as erro:

        print("\nERRO AO PROCESSAR O CENSO")
        print(f"Detalhes: {erro}")
        raise

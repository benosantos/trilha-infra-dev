
import re
import unicodedata



def normalizar_linha(texto):
    """
    Normaliza um telefone brasileiro.

    Aceita:
    - Telefones com DDD e 10 ou 11 dígitos.
    - Telefones com prefixo internacional 55.

    Retorna:
    - OK para telefones válidos.
    - REVISAR para dados inválidos.
    """

    if not isinstance(texto, str) or not texto.strip():
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "telefone vazio ou inválido"
        }

    # Não permite letras ou caracteres especiais inesperados.
    if re.search(r"[^\d\s()+.-]", texto):
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "telefone contém caracteres inválidos"
        }

    digitos = re.sub(r"\D", "", texto)

    # Remove o código do Brasil quando presente.
    if len(digitos) in (12, 13) and digitos.startswith("55"):
        digitos = digitos[2:]

    # Identifica telefone sem DDD.
    if len(digitos) in (8, 9):
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "sem DDD"
        }

    # Verifica a quantidade de dígitos.
    if len(digitos) not in (10, 11):
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "telefone inválido"
        }

    # Verifica o DDD antes de aceitar o telefone.
    ddd = int(digitos[:2])

    if not 11 <= ddd <= 99:
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "DDD inválido"
        }

    return {
        "valor": digitos,
        "status": "OK"
    }


def normalizar_serie(texto):
    """
    Normaliza o número de série de um equipamento.

    Regras:
    - Remove espaços.
    - Converte letras para maiúsculas.
    - Identifica valores desconhecidos.
    - Remove acentos apenas para comparar valores desconhecidos.

    Exemplos:
        pf3a  9x7k -> PF3A9X7K
        Não sei -> REVISAR
    """

    if not isinstance(texto, str):
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "série inválida"
        }

    # Remove espaços e converte para maiúsculas.
    serie = re.sub(r"\s+", "", texto).upper()

    # Remove acentos para comparação.
    serie_sem_acento = unicodedata.normalize(
        "NFKD",
        serie
    ).encode("ASCII", "ignore").decode("ASCII")

    # Valores considerados desconhecidos.
    desconhecidos = [
        "",
        "NAOSEI",
        "-"
    ]

    if serie_sem_acento in desconhecidos:
        return {
            "valor": None,
            "status": "REVISAR",
            "motivo": "série desconhecida"
        }

    return {
        "valor": serie,
        "status": "OK"
    }

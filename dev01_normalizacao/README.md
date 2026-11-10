
# DEV-01 — Normalização de dados

## Objetivo

Normalizar telefones e números de série de equipamentos
informados em formulários de cadastro.

## Tecnologias

- Python 3
- Pytest
- Regex
- Unicodedata

## Estrutura

```text
dev01_normalizacao/
├── src/
│   ├── __init__.py
│   └── normalizacao.py
├── tests/
│   ├── __init__.py
│   └── test_normalizacao.py
└── README.md
```

## Funcionalidades

### normalizar_linha(texto)

- Remove caracteres de formatação.
- Remove o código do país 55.
- Exige DDD.
- Aceita telefones com 10 ou 11 dígitos.
- Retorna REVISAR para entradas inválidas.

### normalizar_serie(texto)

- Remove espaços.
- Converte letras para maiúsculas.
- Identifica séries desconhecidas.
- Trata variações com acentos.

## Como executar

Ative seu ambiente virtual e instale o pytest:

```bash
pip install pytest
```

Execute os testes:

```bash
pytest dev01_normalizacao/tests -v
```

## Critérios de qualidade

- Nenhum dado inválido é descartado silenciosamente.
- Dados desconhecidos recebem status REVISAR.
- Todas as funções possuem testes automatizados.


# DEV-03 — Censo de Equipamentos

## Objetivo

Desenvolver um sistema em Python para processar respostas
de funcionários em CSV e gerar uma lista estruturada
de equipamentos, integrando os desafios DEV-01 e DEV-02.

## Funcionalidades

- Leitura de arquivos CSV.
- Ignorar funcionários cujo nome começa com TESTE.
- Ignorar equipamentos com resposta Não.
- Normalização de telefones.
- Normalização de números de série.
- Integração com DEV-01.
- Integração com DEV-02.
- Geração automática de patrimônios.
- Geração individual de notebooks, celulares e chips.
- Identificadores no formato carimbo#vaga.
- Controle de duplicidade e idempotência.
- Persistência em arquivo JSON.
- Bloqueio de processamento simultâneo.
- Identificação de pendências de revisão.
- Relatório de execução no terminal.

## Tecnologias

- Python
- CSV
- JSON
- Pytest
- Portalocker
- Git
- GitHub

## Estrutura

```text
dev03_censo_equipamentos/
│
├── data/
│   ├── respostas.csv
│   ├── itens.json
│   └── patrimonio_dev03.json
│
├── src/
│   ├── __init__.py
│   ├── leitor_csv.py
│   ├── gerador_itens.py
│   ├── integrador_patrimonio.py
│   ├── persistencia.py
│   └── censo.py
│
├── testes_dev03/
│   ├── __init__.py
│   ├── test_leitor_csv.py
│   ├── test_gerador_itens.py
│   ├── test_integrador_patrimonio.py
│   ├── test_persistencia.py
│   └── test_censo.py
│
└── README.md
```

## Executar o projeto

Ativar ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Executar o censo:

```powershell
python -m dev03_censo_equipamentos.src.censo
```

Executar testes do DEV-03:

```powershell
python -m pytest dev03_censo_equipamentos/testes_dev03 -v
```

Executar todos os testes:

```powershell
python -m pytest -v
```

## Resultado dos testes

- DEV-01: 29 testes aprovados.
- DEV-02: 14 testes aprovados.
- DEV-03: 29 testes aprovados.

Total acumulado: 72 testes aprovados.

## Idempotência

O sistema identifica equipamentos já cadastrados
utilizando o identificador e o tipo do equipamento.

Ao processar novamente o mesmo CSV, os registros
existentes são preservados e não recebem novos
patrimônios.

## Integração

O DEV-03 utiliza as funções desenvolvidas nos desafios
anteriores:

- DEV-01: normalização de telefones e séries.
- DEV-02: geração sequencial de patrimônios.

## Status

Desenvolvimento e testes concluídos.
Pronto para revisão final e publicação no GitHub.

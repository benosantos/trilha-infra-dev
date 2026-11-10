
# DEV-02 — Gerador de Patrimônio

## Objetivo

Desenvolver um gerador de números de patrimônio
para equipamentos de uma empresa.

## Tecnologias

- Python 3
- JSON
- Portalocker
- Pytest
- Multiprocessing

## Formato

PAT-TIPO-NUMERO

Exemplos:

- PAT-NB-0001
- PAT-DT-0001
- PAT-MN-0001
- PAT-CL-0001

## Tipos permitidos

| Código | Equipamento |
|---|---|
| NB | Notebook |
| DT | Desktop |
| MN | Monitor |
| CL | Celular |
| CH | Chip |
| OU | Outros |

## Concorrência

O sistema utiliza Portalocker para bloquear o acesso
ao arquivo JSON durante a atualização do contador.

Isso impede que processos simultâneos gerem
o mesmo número de patrimônio.

## Persistência

Os contadores ficam armazenados em:

data/patrimonio.json

Os números permanecem salvos após reiniciar
o programa.

## Instalação

```bash
pip install portalocker pytest
```

## Executar testes

Na raiz do repositório:

```bash
pytest dev02_patrimonio/tests -v
```

## Teste de concorrência

O teste principal cria 20 processos simultâneos,
cada um gerando 50 patrimônios.

Resultado esperado:

1000 patrimônios únicos, de PAT-NB-0001
até PAT-NB-1000.
